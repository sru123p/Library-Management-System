from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import connection
from django.utils.crypto import get_random_string
from datetime import date
from datetime import timedelta
import bcrypt
# Create your views here.



def logout_request_admin(request):
    # logout(request)
    request.session.clear()
    request.session.flush()
    request.session.clear_expired()
    messages.info(request, "Logged out successfully!")
    return redirect("/admin_login")


def admin_login(request):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    LibrarianID = request.session.get('LibrarianId', 'none')
    if LibrarianID == 'none':
        request.session.flush()
        request.session.clear_expired()
        data = {
                'title' : 'Admin login'
        }

        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM librarians WHERE email= %s""", [email])
            row = cursor.fetchall()
            if cursor.rowcount == 1:
                dbpassword = row[0][3]
                LibrarianId = row[0][0]
                data = {
                'LibrarianId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'title' : 'Admin login'
                }
                
                
                if bcrypt.checkpw(password.encode('utf8'), dbpassword.encode('utf8')):
                    request.session['LibrarianId'] = data['LibrarianId']
                    request.session['name'] = data['name']
                    request.session['email'] = email
                    request.session['loggedinLib'] = True
                    url="admin_login"
                    return redirect(url)
                    # return render(request, 'web_app/index', data)
                
                else:
                    messages.error(request, 'incorrect password please try again!!')
            else:
                messages.error(request, 'Account does not exist with the entered credentials!!!')
        return render(request, 'web_app/admin/login.html')
    else:
        url="admin_home"
        return redirect(url)



def admin_home(request):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request, 'web_app/admin/home.html', data)


def categories_search(request):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
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
            cursor.execute("SELECT authorName FROM book_authors where bookID = %s", [isbn])
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
                'name': request.session.get('name', 'Guest'),
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
        'categories_list': categories_list,
        'name': request.session.get('name', 'Guest'),
    }
    return render(request, 'web_app/admin/categories.html', cat)


def singlebook(request, isbnnumber, author, category):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
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
            'name': request.session.get('name', 'Guest'),
    }
    return render(request, 'web_app/admin/singleBook.html', data)


def issuebook(request):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
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
                'name': request.session.get('name', 'Guest'),
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
                'name': request.session.get('name', 'Guest'),
            }
            return render(request, 'web_app/admin/noissue.html', data)
        else:
            data = {
                'name': request.session.get('name', 'Guest'),
            }
            cursor.execute("select max(due_ID) from dues")
            dueid = cursor.fetchone()
            today = date.today()
            Enddate = today + timedelta(days=30)
            cursor.execute("INSERT INTO dues(due_ID, due_date ) VALUES (%s, %s)",(dueid[0]+1, Enddate ))
            cursor.execute("INSERT INTO borrowed_books( ISBN_book ,copy_num, id_user, issued_date, due_id, status) VALUES (%s, %s, %s, %s, %s, %s)",(isbn, copyno, userid[0], today, dueid[0]+1 , 'borrowed'))
            return render(request, 'web_app/admin/success.html', data)
    return render(request, 'web_app/admin/issuebook.html', data)


def returnbook(request):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
    if request.method == "POST":
        email = request.POST.get("email")
        isbn = request.POST.get("isbn")
        copyno = request.POST.get("copyno")
        cursor = connection.cursor()
        cursor.execute("""SELECT userID FROM users where email = %s """, [email])
        userid = cursor.fetchone()
        if cursor.rowcount == 0:
            data = {
                'name': request.session.get('name', 'Guest'),
            }
            return render(request, 'web_app/admin/nouser.html', data)
        cursor.execute("SELECT * FROM borrowed_books where ISBN_book = %s AND copy_num = %s AND id_user = %s", (isbn, copyno, userid[0]))
        book = cursor.fetchone()
        if cursor.rowcount == 0:
            data = {
                'name': request.session.get('name', 'Guest'),
            }
            return render(request, 'web_app/admin/noreturn.html', data)
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
                'name': request.session.get('name', 'Guest'),
            }
            return render(request, 'web_app/admin/dues.html', data)
        else:
            data = {
                'name': request.session.get('name', 'Guest'),
            }
            cursor.execute("UPDATE borrowed_books SET status='returned' where ISBN_book = %s AND copy_num = %s AND id_user = %s", (isbn, copyno, userid[0]))
            return render(request, 'web_app/admin/success.html', data)
    return render(request, 'web_app/admin/returnbook.html')


def paydues(request, dueid, isbn, userid, copyno):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    today = date.today()
    cursor = connection.cursor()
    cursor.execute("UPDATE dues SET payment_date = %s, payment_method = %s WHERE due_ID = %s", (today, "cash", dueid))
    cursor.execute("UPDATE borrowed_books SET status='returned' where ISBN_book = %s AND copy_num = %s AND id_user = %s", (isbn, copyno, userid))
    return render(request, 'web_app/admin/success.html', data)


def addbook(request):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
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
        'name': request.session.get('name', 'Guest'),
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
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    if request.method == "POST":
        isbn = request.POST.get("isbn")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM books where ISBNNumber = %s AND present=%s""",(int(isbn), "yes"))
        a =cursor.rowcount
        if(a==0):
            return render(request, 'web_app/admin/nobook.html')
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
        cursor.execute("SELECT authorName FROM book_authors where bookID = %s", [int(isbn)])
        author = cursor.fetchall()
        authors = []
        m = cursor.rowcount
        for n in range(m):
            authors.append(author[n-1][0])
        data = {
            'b':b,
            'category':cat,
            'authors':authors,
            'name': request.session.get('name', 'Guest'),
        }
        return render(request, 'web_app/admin/singleBook.html', data)
    return render(request, 'web_app/admin/ISBNsearch.html', data)


def changeshelves(request):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request, 'web_app/admin/success.html', data)


def deletebook(request, isbn):
    if request.session.get('loggedinUser', False) == True:
        return redirect('/')
    if request.session.get('loggedinLib', False) == False:
        return redirect("admin_login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    cursor = connection.cursor()
    cursor.execute("UPDATE books SET present = %s WHERE ISBNnumber = %s", ("no", isbn))
    return render(request, 'web_app/admin/success.html', data)