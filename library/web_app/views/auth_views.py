from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.contrib import messages
# import bcrypt
# import hashlib
# import sys
# import base64
from datetime import datetime
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
# import smtplib
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string


def Sign_Up(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE email = %s""", [email])
        row = cursor.fetchall()
        if cursor.rowcount == 0:
            request.session['username'] = name
            request.session['email'] = email
            request.session['address'] = address
            request.session['password'] = password
            otp = get_random_string(6, allowed_chars='0123456789')
            request.session['otp'] = otp
            send_mail(subject='{} is your Pack your bags OTP'.format(otp),message='click on the below link to Verify your email.Note that this link will only be active for 10minutes.',from_email='cse190001033@iiti.ac.in',recipient_list=[email],fail_silently=True,
            html_message="<h2>Please enter the below OTP to complete your verification.Note that this OTP will only be active for 10minutes.</h2><br><h2>{}</h2>".format(otp))
            request.session['email_link_is_active'] = True
            messages.success(request,'OTP sent to your email please check your inbox!!')
            return redirect('/login/emailverification')
        else:
            messages.success(
                request, 'User with the entered email already exists please login to continue!!!')
            return redirect('/login')
            

    else:
        return render(request, 'web_app/signup.html', {'title': 'create an account'})


def login(request):
    request.session.flush()
    request.session.clear_expired()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE email= %s""", [email])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][6]
            userId = row[0][7]
            data = {
            'firstname': row[0][0],
            'lastname': row[0][1],
            'gender': row[0][2],
            'address': row[0][3],
            'mobileno': row[0][4],
            'email': row[0][5],
            'password': row[0][6],
            'userId': row[0][7],
            'DOB': row[0][8],
            'role':row[0][10]
             }
            if bcrypt.checkpw(password.encode('utf8'), dbpassword.encode('utf8')):
               
                request.session['userId'] = row[0][7]
                if data["role"]=="admin":
                    messages.success(request, 'Login successful!!')
                    request.session['email'] = email
                    request.session['role'] = data['role']
                    url = "/admin/home"
                    return redirect(url)
                elif data["role"]=='user':
                    messages.success(request, 'Login successful!!')
                    request.session['email'] = email
                    request.session['role'] = data['role']
                    url="/home"
                    return redirect(url)
               
            else:
              
                 messages.success(request, 'incorrect password please try again!!')
                 return render(request, 'authentication/login.html')
        else:
            messages.success(request, 'Account does not exist with the entered credentials!! signup to create an account')
            return render(request, 'authentication/login.html')
    else:
        return render(request, 'authentication/login.html')
