from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'web_app/index.html', {'title' : 'home'})

def login(request):
    return render(request, 'web_app/login.html', {'title' : 'login'})
