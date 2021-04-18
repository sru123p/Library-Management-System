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
    path('shop', views_r.shop, name = 'shop'),
    path('checkout', views_r.checkout, name = 'checkout'),
    path('single_product', views_r.single_product, name = 'single_product'),
]
