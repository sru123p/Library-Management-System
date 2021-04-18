from django.urls import path
from .views import views_r
from .views import views_a
from .views import views_m
from .views import views_s

urlpatterns = [
    path('', views_r.home, name = 'home'),
    path('login', views_r.login, name = 'login'),
    path('cart', views_r.cart, name = 'cart'),
    path('signup', views_r.signup, name = 'signup'),
    path('category', views_r.category, name = 'category'),
    path('checkout', views_r.checkout, name = 'checkout'),
    path('single_book', views_r.single_book, name = 'single_book'),
    
]
