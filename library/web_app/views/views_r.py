import bcrypt
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string


# Create your views here.


def logout_request(request):
    # logout(request)
    request.session.clear()
    request.session.flush()
    request.session.clear_expired()
    messages.info(request, "Logged out successfully!")
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
                'title' : 'Dashboard',
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
            if request.method == "POST":
                rating = request.POST.get('rating')
                cursor1 = connection.cursor()
                book_ID = books[0][0]
                cursor1.execute("""SELECT * FROM ratings WHERE user_ID = %s AND book_ID= %s""",[userID,book_ID])
                if cursor1.rowcount ==0:
                    cursor1.execute("""INSERT INTO ratings(user_ID,book_ID,rating) VALUES (%s, %s, %s)""",[userIDbook_ID,rating])
                else:
                    cursor1.execute("""UPDATE ratings SET rating = %s  WHEREuser_ID = %s AND book_ID= %d""",[rating,userID,book_ID])
    return render(request, 'web_app/ratings.html',{'books' : books, 'title' : 'Ratings','userId': row[0][0],'name': row[0][1]})

def friends(request):
    userID = request.session.get('userId', 'none')
    if userID != 'none':
        cursor = connection.cursor()
        cursor.execute("""SELECT name2,accepted FROM friends WHERE f1ID= %s""", [userID])
        friend = cursor.fetchall()
    return render(request, 'web_app/friends.html', {'friend': friend, 'title' : 'myfriends'})


