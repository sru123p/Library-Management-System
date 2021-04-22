from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'web_app/index.html', {'title' : 'home'})

def login(request):
    return render(request, 'web_app/login.html', {'title' : 'login'})

def signup(request):
    return render(request, 'web_app/signup.html', {'title' : 'signup'})

def cart(request):
    return render(request, 'web_app/cart.html', {'title' : 'cart'})

def category(request):
    return render(request, 'web_app/category.html', {'title' : 'category'})

def checkout(request):
    return render(request, 'web_app/checkout.html', {'title' : 'checkout'})

def single_book(request):
    return render(request, 'web_app/single_book.html', {'title' : 'single_book'})
