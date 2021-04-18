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

def shop(request):
    return render(request, 'web_app/shop.html', {'title' : 'shop'})

def checkout(request):
    return render(request, 'web_app/checkout.html', {'title' : 'checkout'})

def single_product(request):
    return render(request, 'web_app/single-product.html', {'title' : 'single_product'})