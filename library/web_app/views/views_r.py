import bcrypt
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string


# Create your views here.


def email_all(request):
    cursor = connection.cursor()
    cursor.execute("""select id_user, copy_num from borrowed_books where issued_date  <= NOW() - INTERVAL 15 DAY and status = 'borrowed'""",)
    print(cursor.rowcount)
    row = cursor.fetchall()
    a = cursor.rowcount
    userId = 1
    BookID = 0
    cursor.execute("""SELECT * FROM users WHERE userID= %s""", [userId])
    row1 = cursor.fetchall()
    email = row1[0][2]
    userName = row1[0][1]
    send_mail(
                subject='Remainder mail from IIT indore Library to user[{}]'.format(userId),
                message='click on the below link to Verify your email.',
                from_email='cse19000101051@iiti.ac.in',
                recipient_list=[email],
                fail_silently=True,
                html_message="Dear user you have not returned your book of ISBN Number #{} it has been more than 15 days.".format(BookID)
                )
    if a!=0:
            for i in range(a):
                userId = row[i][2]
                BookID = row[i][0]

                cursor.execute("""SELECT * FROM users WHERE userID= %s""", [userId])
                row = cursor.fetchall()
                email = row1[0][2]
                userName = row1[0][1]
                send_mail(
                subject='Remainder mail from IIT indore Library to #{} '.format(userId),
                message='click on the below link to Verify your email.',
                from_email='cse19000101051@iiti.ac.in',
                recipient_list=[email],
                fail_silently=True,
                html_message="Dear user you have not returned your book of ISBN Number #{} it has been more than 15 days.".format(BookID)
                )
    messages.success(request, "Email sent Successfully!")
    return redirect('/admin_home')
    

def logout_request(request):
    # logout(request)
    request.session.clear()
    request.session.flush()
    request.session.clear_expired()
    messages.info(request, "Logged out successfully!")
    return redirect("/login")

def delete_account(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM users WHERE userId= %s""", [userID])
        request.session.clear()
        request.session.flush()
        request.session.clear_expired()
        return redirect("/login")
    else:
        return redirect("/login")

def resend_OTP(request):
    email = request.session.get('email')
    otp = get_random_string(6, allowed_chars='0123456789')
    request.session['otp'] = otp
                
    send_mail(
        subject='{} is your IIT Indore Library OTP'.format(otp),
        message='click on the below link to Verify your email.',
        from_email='cse19000101051@iiti.ac.in',
        recipient_list=[email],
        fail_silently=True,
        html_message="<p>Please enter the below OTP to complete your verification.</p><h3>{}</h3>".format(otp)
        )
    
    request.session['email_link_is_active'] = True
    messages.success(request,'OTP sent to your email please check your inbox!!')
    return redirect("/otp_verification")


def otp_verification(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    userID = request.session.get('userId', 'none')
    if userID == 'none':
        if request.method =='POST':
            otp = request.POST.get('otp')
            cursor = connection.cursor()
            if request.session.get('otp')!=None:
                otp_from_email = request.session.get('otp')
                if otp == otp_from_email:
                    name = request.session.get('name')
                    email = request.session.get('email')
                    address = request.session.get('address')
                    password = request.session.get('password')
                    password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(rounds=12))
                    userID = 1
                    cursor.execute("""SELECT * FROM users WHERE userID = (SELECT MAX(userID) FROM users) """)
                    if cursor.rowcount ==0:
                        userID = 1
                    else:
                        row = cursor.fetchall()
                        userID = row[0][0]+1
                    cursor.execute("""INSERT INTO users( userID ,Name, email, password, address, role) VALUES (%s, %s, %s, %s, %s, %s)""",(userID,name, email, password, address, 'student'))
                    messages.success(request,'verification successful!!please  login to continue')
                    return redirect('/login')
                else:
                    messages.error(request,'invalid otp try again!!')

            else:
                messages.error(request,'Signup before email verification!!')
                return redirect('/signup')
        return render(request, 'web_app/otp_verification.html', {'title': 'otp verification'})
    else :
        url = "/"
        return redirect(url)


def signup(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    userID = request.session.get('userId', 'none')
    if userID == 'none':
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            password = request.POST.get('password')
            
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM users WHERE email = %s""", [email])
            otp = get_random_string(6, allowed_chars='0123456789')
            request.session['otp'] = otp
            row = cursor.fetchall()
            if cursor.rowcount == 0:
                request.session['name'] = name
                request.session['email'] = email
                request.session['address'] = address
                request.session['password'] = password
                # request.session['password'] = sha256_crypt.encrypt(password)
                
                otp = get_random_string(6, allowed_chars='0123456789')
                request.session['otp'] = otp
                
                send_mail(
                    subject='{} is your IIT Indore Library OTP'.format(otp),
                    message='click on the below link to Verify your email.Note that this link will only be active for 10minutes.',
                    from_email='cse19000101051@iiti.ac.in',
                    recipient_list=[email],
                    fail_silently=True,
                    html_message="<p>Please enter the below OTP to complete your verification.Note that this OTP will only be active for 10minutes.</p><h3>{}</h3>".format(otp)
                    )
                
                request.session['email_link_is_active'] = True
                messages.success(request,'OTP sent to your email please check your inbox!!')
                return redirect('/otp_verification')
            else:
                messages.success(request, 'User with the entered email already exists please login to continue!!!')
                return redirect('/login')

        return render(request, 'web_app/signup.html', {'title' : 'create an account'})
    else :
        url = "/"
        return redirect(url)


def login(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    userID = request.session.get('userId', 'none')
    if userID == 'none':
        request.session.flush()
        request.session.clear_expired()
        data = {
                'title' : 'login'
        }

        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM users WHERE email= %s""", [email])
            row = cursor.fetchall()
            if cursor.rowcount == 1:
                dbpassword = row[0][3]
                userId = row[0][0]
                data = {
                'userId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'role':row[0][5],
                'title' : 'login'
                }
                
                if bcrypt.checkpw(password.encode('utf8'), dbpassword.encode('utf8')):
                    request.session['userId'] = data['userId']
                    request.session['name'] = data['name']
                    request.session['email'] = email
                    request.session['role'] = data['role']
                    request.session['loggedinUser'] = True
                    url="/"
                    return redirect(url)
                    # return render(request, 'web_app/index.html', data)
                
                else:
                    messages.error(request, 'incorrect password please try again!!')
            else:
                messages.error(request, 'Account does not exist with the entered credentials!! signup to create an account')
        return render(request, 'web_app/login.html', data)
    else:
        url="/"
        return redirect(url)


    
def home(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
                'name': request.session.get('name', 'Guest'),
                'title' : 'home',
            }
    return render(request, 'web_app/index.html', data )



def userdashboard(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userId= %s""", [userID])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][3]
            userId = row[0][0]
            data = {
                'userId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'role':row[0][5],
                'title' : 'userdashboard',
                }
    return render(request, 'web_app/userdashboard.html', data)

def ratings(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userId= %s""", [userID])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][3]
            userId = row[0][0]
            data = {
                'userId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'role':row[0][5],
                'title' : 'Ratings',
                }
            cur = connection.cursor()
            cur.execute("""SELECT * FROM borrowed_books WHERE id_user= %s""", [userID])
            books = cur.fetchall()
            cur1 = connection.cursor()
            cur1.execute("""SELECT title, ISBNnumber, copyNo FROM books WHERE ISBNnumber in (SELECT ISBN_book FROM borrowed_books WHERE id_user= %s) and copyNo in (SELECT copy_num FROM borrowed_books WHERE id_user= %s)""", [userID,userID])
            details = cur1.fetchall()
            if request.method == "POST":
                rating = request.POST.get('rating')
                review = request.POST.get('review')
                cursor1 = connection.cursor()
                book_ID = books[0][0]
                cursor1.execute("""SELECT * FROM ratings_reviews WHERE user_ID = %s AND book_ID= %s""",[userID,book_ID])
                if cursor1.rowcount ==0:
                    cursor1.execute("""INSERT INTO ratings_reviews(user_ID,book_ID,rating,review) VALUES (%s, %s, %s,%s)""",[userID,book_ID,rating,review])
                else:
                    cursor1.execute("""UPDATE ratings SET rating = %s, review =%s WHERE user_ID = %s AND book_ID= %d""",[rating,review,userID,book_ID])
    return render(request, 'web_app/ratings.html',{'books' : books, 'details' : details, 'title' : 'Ratings','userId': row[0][0],'name': row[0][1]})

def friends(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userId= %s""", [userID])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][3]
            userId = row[0][0]
            data = {
                'userId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'role':row[0][5],
                'title' : 'My Friends',
                }
    userID = request.session.get('userId', 'none')
    if request.method == "POST":
        user1 = request.POST.get('user1')
        cursor1 = connection.cursor()
        cursor1.execute("""SELECT * FROM borrowed_books WHERE id_user=%s""",[user1])
        books=cursor1.fetchall()
        if userID != 'none':
            cur2 = connection.cursor()
            cur2.execute("""SELECT * FROM users WHERE userID in (SELECT f2ID from friends WHERE f1ID= %s)""", [userID])
            friend=cur2.fetchall()
            return render(request, 'web_app/friends.html', {'friend': friend, 'books' : books, 'title' : 'My Friends', 'userId': row[0][0],'name': row[0][1]})  
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userID in (SELECT f2ID from friends WHERE f1ID= %s)""", [userID])
        friend = cursor.fetchall()  
        return render(request, 'web_app/friends.html', {'friend': friend, 'title' : 'My Friends', 'userId': row[0][0],'name': row[0][1]})

def find_friends(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userId= %s""", [userID])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][3]
            userId = row[0][0]
            data = {
                'userId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'role':row[0][5],
                'title' : 'Find others',
                }
    userID = request.session.get('userId', 'none')
    if request.method == "POST":
        user2 = request.POST.get('user2')
        cursor1 = connection.cursor()
        cursor1.execute("""INSERT INTO temp_request(user1ID, user2ID) values (%s,%s)""",[userID,user2])
        if userID != 'none':
            cur = connection.cursor()
            cur.execute("""SELECT * FROM users WHERE userID <> %s""", [userID])
            friend = cur.fetchall()
            return render(request, 'web_app/find_friends.html', {'friend': friend, 'title' : 'Find Others', 'userId': row[0][0],'name': row[0][1]})
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userID <> %s""", [userID])
        friend = cursor.fetchall()
    return render(request, 'web_app/find_friends.html', {'friend': friend, 'title' : 'Find Others', 'userId': row[0][0],'name': row[0][1]})

def pending(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userId= %s""", [userID])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][3]
            userId = row[0][0]
            data = {
                'userId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'role':row[0][5],
                'title' : 'Pending Requests',
                }
    userID = request.session.get('userId', 'none')
    if request.method == "POST":
        user1 = request.POST.get('user1')
        cursor1 = connection.cursor()
        cursor1.execute("""INSERT INTO friends(f1ID, f2ID) values (%s,%s)""",[userID,user1])
        cur1 = connection.cursor()
        cur1.execute("""DELETE FROM temp_request WHERE user2ID=%s AND user1ID=%s""",[userID,user1])
        if userID != 'none':
            cur2 = connection.cursor()
            cur2.execute("""SELECT * FROM users WHERE userID in (SELECT user1ID FROM temp_request WHERE user2ID=%s)""", [userID])
            friend=cur2.fetchall()
            return render(request, 'web_app/pending.html', {'friend': friend, 'title' : 'Pending Requests', 'userId': row[0][0],'name': row[0][1]})
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userID in (SELECT user1ID FROM temp_request WHERE user2ID=%s)""", [userID])
        friend = cursor.fetchall()
    return render(request, 'web_app/pending.html', {'friend': friend, 'title' : 'Pending Requests', 'userId': row[0][0],'name': row[0][1]})

def borrowed_books(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userId= %s""", [userID])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][3]
            userId = row[0][0]
            data = {
                'userId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'role':row[0][5],
                'title' : 'Borrowed Books',
                }
    userID = request.session.get('userId', 'none')
    
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM borrowed_books WHERE id_user=%s""", [userID])
        books = cursor.fetchall()
    return render(request, 'web_app/borrowed_books.html', {'books': books, 'title' : 'Borrowed Books', 'userId': row[0][0],'name': row[0][1]})

def bookshelf(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userId= %s""", [userID])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][3]
            userId = row[0][0]
            data = {
                'userId': row[0][0],
                'name': row[0][1],
                'email': row[0][2],
                'password': row[0][3],
                'address': row[0][4],
                'role':row[0][5],
                'title' : 'My Bookshelf',
                }
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM personal_bookshelf WHERE iduser=%s""", [userID])
        book = cursor.fetchall()
    return render(request, 'web_app/bookshelf.html', {'book': book, 'title' : 'My Bookshelf', 'userId': row[0][0],'name': row[0][1]})

