from django.urls import path
from .views import views_r
from .views import views_a
from .views import views_m
from .views import views_s

urlpatterns = [
    path('', views_r.home, name = 'home'),
    path('login', views_r.login, name = 'login'),
    path('admin_login', views_r.admin_login, name = 'admin_login'),
    path('logout', views_r.logout_request, name = 'logout'),
    path('admin_logout', views_r.logout_request_admin, name = 'admin_logout'),
    path('userdashboard', views_r.userdashboard, name = 'userdashboard'),
    path('ratings', views_r.ratings, name = 'ratings'),
    path('cart', views_r.cart, name = 'cart'),
    path('signup', views_r.signup, name = 'signup'),
    path('category', views_r.category, name = 'category'),
    path('checkout', views_r.checkout, name = 'checkout'),
    path('single_book', views_r.single_book, name = 'single_book'),
    path('admin_home', views_s.admin_home, name='admin_home'),
    path('categories_search', views_s.categories_search, name='categories_search'),
    path('singlebook/<isbnnumber>/<author>/<category>', views_s.singlebook, name = 'singlebook'),
    path('issuebook', views_s.issuebook, name='issuebook'),
    path('returnbook', views_s.returnbook, name='returnbook'),
    path('paydues/<request>/<dueid>/<isbn>/<userid>/<copyno>',views_s.paydues ,name = 'paydues'),
    path('addbook', views_s.addbook, name='addbook'),
    path('isbnsearch', views_s.isbnsearch, name='isbnsearch'),
    path('changeshelves', views_s.changeshelves, name='changeshelves'),
    path('deletebook', views_s.deletebook, name='deletebook'),
]
