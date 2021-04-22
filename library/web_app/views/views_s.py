from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from datetime import date
from datetime import timedelta
# Create your views here.

def admin_home(request):
    return render(request, 'web_app/admin/home.html')


def categories_search(request):
    if request.method == "POST":
        catname = request.POST.get("catname")
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT bookISBN FROM category where category_name = %s """, [catname])
        ISBN = cursor.fetchall()
        b=[]
        for isbn in ISBN:
            cursor = connection.cursor()
            cursor.execute("SELECT ISBNnumber, title, publication_year, count(*) FROM books where ISBNnumber = %s AND present=%s GROUP BY ISBNnumber", (isbn,"yes"))
            books = cursor.fetchall()
            cursor = connection.cursor()
            cursor.execute("SELECT authorName FROM book_authors where bookID", [isbn])
            authors = cursor.fetchall()
            author = []
            a = cursor.rowcount
            for n in range(a):
                author.append(authors[n-1][0])
            print(books[0])
            b.append({
                     'ISBN':books[0][0],
                     'title':books[0][1],
                     'pub_year':books[0][2],
                     'count':books[0][3],
                     'author':author,
                 })
        data = {
                'b':b,
                'category': catname,
             }
        return render(request, 'web_app/admin/singlecat.html', data)
    cursor = connection.cursor()
    cursor.execute("""SELECT DISTINCT Category_name FROM category order by Category_name""")
    categories = cursor.fetchall()
    categories_list = []
    for catn in categories:
        for ca in catn:
            categories_list.append(ca)
    cat = {
        'categories_list': categories_list
    }
    return render(request, 'web_app/admin/categories.html', cat)


def singlebook(request, isbnnumber, author, category):
    cursor = connection.cursor()
    cursor.execute("SELECT ISBNnumber, title, publication_year, count(*) FROM books where ISBNnumber = %s GROUP BY ISBNnumber", [isbnnumber])
    books = cursor.fetchall()
    authors = list(author)
    b=[]
    b.append({
            'ISBN':books[0][0],
            'title':books[0][1],
            'pub_year':books[0][2],
            'count':books[0][3],
    })
    data = {
            'b':b,
            'category':category,
            'authors':authors,
    }
    return render(request, 'web_app/admin/singleBook.html', data)


def issuebook(request):
    if request.method == "POST":
        email = request.POST.get("email")
        isbn = request.POST.get("isbn")
        copyno = request.POST.get("copyno")
        cursor = connection.cursor()
        cursor.execute("""SELECT userID, role FROM users where email = %s """, [email])
        userid = cursor.fetchone()
        if cursor.rowcount == 0:
            return render(request, 'web_app/admin/nouser.html')
        cursor.execute("SELECT due_id FROM borrowed_books where id_user = %s AND status = %s", (userid[0],"borrowed"))
        dues = cursor.fetchall()
        a = cursor.rowcount
        st = '3 books are already on loan'
        if a == 3 and userid[1] == "student":
            data = {
                'd' : st,
            }
            return render(request, 'web_app/admin/noissue.html', data)
        fines = 0
        for x in range(a):
            cursor.execute("""SELECT due_date FROM dues where due_ID = %s """, [ dues[x][0] ])
            issdate = cursor.fetchone()
            today = date.today()
            cursor.execute("""SELECT DATEDIFF(%s, %s)""", (today , issdate[0]))
            days = cursor.fetchone()
            if(days[0] > 0):
                fines = fines + days[0]*5
        print(fines)
        st = 'Your fine exceeds 1000'
        if(fines > 1000):
            data = {
                'd' : st,
                'f' : fines,
            }
            return render(request, 'web_app/admin/noissue.html', data)
        else:
            cursor.execute("select max(due_ID) from dues")
            dueid = cursor.fetchone()
            today = date.today()
            Enddate = today + timedelta(days=30)
            cursor.execute("INSERT INTO dues(due_ID, due_date ) VALUES (%s, %s)",(dueid[0]+1, Enddate ))
            cursor.execute("INSERT INTO borrowed_books( ISBN_book ,copy_num, id_user, issued_date, due_id, status) VALUES (%s, %s, %s, %s, %s, %s)",(isbn, copyno, userid[0], today, dueid[0]+1 , 'borrowed'))
            return render(request, 'web_app/admin/success.html')
    return render(request, 'web_app/admin/issuebook.html')


def returnbook(request):
    if request.method == "POST":
        email = request.POST.get("email")
        isbn = request.POST.get("isbn")
        copyno = request.POST.get("copyno")
        cursor = connection.cursor()
        cursor.execute("""SELECT userID FROM users where email = %s """, [email])
        userid = cursor.fetchone()
        if cursor.rowcount == 0:
            return render(request, 'web_app/admin/nouser.html')
        cursor.execute("SELECT * FROM borrowed_books where ISBN_book = %s AND copy_num = %s AND id_user = %s", (isbn, copyno, userid[0]))
        book = cursor.fetchone()
        if cursor.rowcount == 0:
            return render(request, 'web_app/admin/noreturn.html')
        cursor.execute("""SELECT due_date FROM dues where due_ID = %s """, [book[4]])
        dues = cursor.fetchone()
        today = date.today()
        cursor.execute("""SELECT DATEDIFF(%s, %s)""", (today ,dues[0]))
        days = cursor.fetchone()
        if(days[0] > 0 ):
            fine = days[0]*5
            cursor.execute("UPDATE dues SET fine_amount = %s WHERE due_ID = %s", (fine, book[4]))
            data = {
                'fine': fine,
                'days': days[0],
            }
            return render(request, 'web_app/admin/dues.html', data)
        else:
            cursor.execute("UPDATE borrowed_books SET status='returned' where ISBN_book = %s AND copy_num = %s AND id_user = %s", (isbn, copyno, userid[0]))
            return render(request, 'web_app/admin/success.html')
    return render(request, 'web_app/admin/returnbook.html')


def paydues(request, dueid, isbn, userid, copyno):
    today = date.today()
    cursor = connection.cursor()
    cursor.execute("UPDATE dues SET payment_date = %s, payment_method = %s WHERE due_ID = %s", (today, "cash", dueid))
    cursor.execute("UPDATE borrowed_books SET status='returned' where ISBN_book = %s AND copy_num = %s AND id_user = %s", (isbn, copyno, userid))
    return render(request, 'web_app/admin/success.html')


def addbook(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT DISTINCT Category_name FROM category order by Category_name""")
    categories = cursor.fetchall()
    categories_list = []
    for catn in categories:
        for ca in catn:
            categories_list.append(ca)
    cursor = connection.cursor()
    cursor.execute("""SELECT DISTINCT shelfID FROM shelf order by shelfID""")
    shelves = cursor.fetchall()
    shelf_list = []
    for catn in shelves:
        for ca in catn:
            shelf_list.append(ca)
    cat = {
        'categories_list': categories_list,
        'shelf_list' : shelf_list,
    }
    if request.method == "POST":
        name = request.POST.get("name")
        isbn = request.POST.get("isbn")
        author1 = request.POST.get("author1")
        author2 = request.POST.get("author2")
        author3 = request.POST.get("author3")
        copies = request.POST.get("copies")
        cat = request.POST.get("catname")
        shelfid = request.POST.get("shelfid")
        cursor = connection.cursor()
        for a in range(int(copies)):
            cursor.execute("INSERT INTO books (ISBNnumber, copyNo, title, shelfID) VALUES ( %s, %s, %s, %s)",(int(isbn), a+1, name, int(shelfid)))
        cursor = connection.cursor()
        if(author1):
            cursor.execute("INSERT INTO book_authors(bookID, authorName) VALUES (%s, %s)",(int(isbn), author1))
        if(author2):
            cursor.execute("INSERT INTO book_authors(bookID, authorName) VALUES (%s, %s)",(int(isbn), author2))
        if(author3):
            cursor.execute("INSERT INTO book_authors(bookID, authorName) VALUES (%s, %s)",(int(isbn), author3))
        return render(request, 'web_app/admin/success.html')
    return render(request, 'web_app/admin/addbooks.html', cat)

def isbnsearch(request):
    if request.method == "POST":
        isbn = request.POST.get("isbn")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM books where ISBNNumber = %s AND present=%s""",(int(isbn), "yes"))
        a =cursor.rowcount
        books = cursor.fetchone()
        cursor.execute("""SELECT Category_name FROM category where bookISBN = %s""",[int(isbn)])
        cat = cursor.fetchall()
        b=[]
        b.append({
                'ISBN':books[0],
                'title':books[2],
                'pub_year':books[3],
                'shelfID':books[4],
                'count':a,
        })
        cursor.execute("SELECT authorName FROM book_authors where bookID", [int(isbn)])
        author = cursor.fetchall()
        authors = []
        m = cursor.rowcount
        for n in range(m):
            authors.append(author[n-1][0])
        data = {
            'b':b,
            'category':cat,
            'authors':authors,
        }
        return render(request, 'web_app/admin/singleBook.html', data)
    return render(request, 'web_app/admin/ISBNsearch.html')


def changeshelves(request):
    
    return render(request, 'web_app/admin/success.html')


def deletebook(request, isbn):
    cursor = connection.cursor()
    cursor.execute("UPDATE books SET present = %s WHERE ISBNnumber = %s", ("no", isbn))
    return render(request, 'web_app/admin/success.html')