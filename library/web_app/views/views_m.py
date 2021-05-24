
from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.contrib import messages
import bcrypt
import hashlib
import sys
import base64
from datetime import datetime
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
import smtplib

# Create your views here.

def titcategory(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request, 'web_app/titcategory.html', data)

def titlesearch(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    if request.method=='GET':
        val = request.GET["title"]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM Books where title =%s """,[val])
        print(cursor.rowcount)
        row = cursor.fetchall()
        books=[]
        data={
            'books':None
        }
        a = cursor.rowcount
        if a!=0:
             for n in range(a):
                 books.append({
                     'isbnnumber':row[n][0],
                     'name':row[n][2],
                     'copyno':row[n][1],
                     'status':row[n][5],
                 })

             data = {
                'books':books,
            
             }
        return render(request,'web_app/titlesearch.html',data)

def authcategory(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request, 'web_app/authcategory.html', data)
    
def authsearch(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    if request.method=='GET':
        val = request.GET["auth"]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM books where  auth_name= %s""", [val])
        print(cursor.rowcount)
        row = cursor.fetchall()
        books=[]
        data={
            'books':None
        }
        a = cursor.rowcount
        if a!=0:
             for n in range(a):
                 books.append({
                     'isbnnumber':row[n][0],
                     'name':row[n][2],
                     'copy':row[n][1],
                     'status':row[n][5],
                 })
             data = {
                'books':books,
                'name': request.session.get('name', 'Guest'),
            
             }
        return render(request,'web_app/authsearch.html',data)  

def single_book(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
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
    if request.method == "POST":
        ISBN = request.POST.get('ISBN')
        cursor1 = connection.cursor()
        cursor1.execute("""INSERT INTO personal_bookshelf(iduser, ISBNbook) values (%s,%s)""",[userID,ISBN])
        if userID != 'none':
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM personal_bookshelf WHERE iduser = %s""",[userID])
            book = cursor.fetchall()
            return render(request, 'web_app/bookshelf.html', {'book': book, 'title' : 'My Bookshelf', 'userId': row[0][0],'name': row[0][1]})

    if request.method=='GET':
        value = request.GET["bookauth"]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM books where  title= %s""", [value])
        print(cursor.rowcount)
        row = cursor.fetchall()
        books=[]
        data={
            'books':None,
            'name': request.session.get('name', 'Guest'),
        }
        a = cursor.rowcount
        if a!=0:
             for n in range(a):
                 books.append({
                     'isbnnumber':row[n][0],
                     'name':row[n][2],
                     'copy':row[n][1],
                     'status':row[n][5],
                     
                 })

             data = {
                'books':books,
                'name': request.session.get('name', 'Guest'),
             }
        return render(request,'web_app/single_book.html',data)  

def favorites(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request,'web_app/favorites.html', data)  

def cont(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request,'web_app/cont.html', data) 

def issuedbooks(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request,'web_app/issuedbooks.html', data)    

def fines(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request,'web_app/fines.html', data)   

def single_bookm(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
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
    if request.method == "POST":
        ISBN = request.POST.get('ISBN')
        cursor1 = connection.cursor()
        cursor1.execute("""INSERT INTO personal_bookshelf(iduser, ISBNbook) values (%s,%s)""",[userID,ISBN])
        if userID != 'none':
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM personal_bookshelf WHERE iduser = %s""",[userID])
            book = cursor.fetchall()
            return render(request, 'web_app/bookshelf.html', {'book': book, 'title' : 'My Bookshelf', 'userId': row[0][0],'name': row[0][1]})

    return render(request,'web_app/single_bookm.html', data)

def isslist(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    if request.method=='GET':
        issid = request.GET["iss"]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM borrowed_books where  id_user= %s""", [issid])
        print(cursor.rowcount)
        row = cursor.fetchall()
        books=[]
        data={
            'books':None,
            'name': request.session.get('name', 'Guest'),
        }
        a = cursor.rowcount
        if a!=0:
             for n in range(a):
                 books.append({
                     'isbnnum':row[n][0],
                     'copy':row[n][1],
                     'issued_date':row[n][3],
                     'status':row[n][5],
                 })

             data = {
                'books':books,
                'name': request.session.get('name', 'Guest'),
    
             }
        return render(request,'web_app/isslist.html',data)  

def fineslist(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    if request.method=='GET':
        fineid = request.GET["fine"]
        cursor = connection.cursor()
        cursor.execute("""select dues.due_ID,dues.fine_amount,borrowed_books.ISBN_book from dues join borrowed_books on dues.due_id = borrowed_books.due_id where borrowed_books.id_user = %s""", [fineid])
        print(cursor.rowcount)
        row = cursor.fetchall()
        books=[]
        data={
            'books':None,
            'name': request.session.get('name', 'Guest'),
        }
        a = cursor.rowcount
        if a!=0:
             for n in range(a):
                 books.append({
                     'fineamount':row[n][1],
                     'isbnnumb':row[n][2],
                     'dueid':row[n][0],
                 })

             data = {
                'books':books,
            
             }
        return render(request,'web_app/fineslist.html',data)  

def payingfine(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request,'web_app/payingfine.html', data)

def clearfine(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    if request.method=='GET':
        did = request.GET["uid"]
        cursor = connection.cursor()
        cursor.execute("""update dues SET fine_amount='0' WHERE due_ID=%s""", [did])
        return render(request,'web_app/success.html', data) 

def hold(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request,'web_app/hold.html', data)  

def log(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    return render(request, 'log.html', data)          

def holdfill(request):
    if request.session.get('loggedinLib', False) == True:
        return redirect('/admin_home')
    if request.session.get('loggedinUser', False) == False:
        return redirect("login")
    data = {
        'name': request.session.get('name', 'Guest'),
    }
    if request.method=='GET':
        usid = request.GET['usid']
        boid = request.GET['boid']
        conu = request.GET["conu"]
        rol= request.GET["rol"]
        now = datetime.now()
        now = now.strftime("%Y-%m-%d")
        cursor = connection.cursor()
        try:
          cursor.execute("""select max(due_ID) from dues""")  
          duei = cursor.fetchone()
          cursor.execute("""INSERT INTO dues(due_ID,due_date,fine_amount,payment_date,payment_method) VALUES (%s,%s,%s,%s,%s)""",(duei[0]+1,'0000-00-00','0','0000-00-00','null'))
          cursor.execute("""INSERT INTO borrowed_books(ISBN_book,copy_num,id_user,issued_date,due_id,status,role) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(boid,conu,usid,now,duei[0]+1,'on hold',rol))      
        finally:
            cursor.close()
        return render(request,'web_app/success.html', data)     