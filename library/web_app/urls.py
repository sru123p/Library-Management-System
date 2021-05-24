from django.urls import path
from .views import views_r
from .views import views_a
from .views import views_m
from .views import views_s
from django.conf.urls import (
handler404
)

# handler404 = 'web_app.views_r.home'

urlpatterns = [
    
    path('', views_r.home, name = 'home'),
    path('login', views_r.login, name = 'login'),
    path('admin_login', views_s.admin_login, name = 'admin_login'),
    path('logout', views_r.logout_request, name = 'logout'),
    path('admin_logout', views_s.logout_request_admin, name = 'admin_logout'),
    path('userdashboard', views_r.userdashboard, name = 'userdashboard'),
    path('ratings', views_r.ratings, name = 'ratings'),
    path('friends', views_r.friends, name = 'friends'),
    path('borrowed_books', views_r.borrowed_books, name = 'borrowed_books'),
    path('pending', views_r.pending, name = 'pending'),
    path('bookshelf', views_r.bookshelf, name = 'bookshelf'),
    path('find_friends', views_r.find_friends, name = 'find_friends'),
    path('delete_account', views_r.delete_account, name = 'delete_account'),
    path('signup', views_r.signup, name = 'signup'),
    path('admin_home', views_s.admin_home, name='admin_home'),
    path('categories_search', views_s.categories_search, name='categories_search'),
    path('singlebook/<isbnnumber>/<author>/<category>', views_s.singlebook, name = 'singlebook'),
    path('issuebook', views_s.issuebook, name='issuebook'),
    path('returnbook', views_s.returnbook, name='returnbook'),
    path('paydues/<request>/<dueid>/<isbn>/<userid>/<copyno>',views_s.paydues ,name = 'paydues'),
    path('addbook', views_s.addbook, name='addbook'),
    path('isbnsearch', views_s.isbnsearch, name='isbnsearch'),
    path('changeshelves', views_s.changeshelves, name='changeshelves'),
    path('deletebook/<isbn>', views_s.deletebook, name='deletebook'),
    path('otp_verification', views_r.otp_verification, name = 'otp_verification'),
    path('resend_OTP', views_r.resend_OTP, name = 'resend_OTP'),
    path('titcategory',views_m.titcategory,name = 'titcategory'),
    path('titlesearch',views_m.titlesearch,name = 'titlesearch'),
    path('authcategory',views_m.authcategory,name = 'authcategory'),
    path('authsearch',views_m.authsearch,name = 'authsearch'),
    path('single_book',views_m.single_book, name = 'single_book'),
    path('single_bookm',views_m.single_bookm, name = 'single_bookm'),
    path('cont',views_m.cont,name = 'cont'),
    path('favorites',views_m.favorites,name='favorites'),
    path('issuedbooks',views_m.issuedbooks,name='issuedbooks'),
    path('isslist',views_m.isslist,name = 'isslist'),
    path('fines',views_m.fines,name = 'fines'),
    path('fineslist',views_m.fineslist,name = 'fineslist'),
    path('payingfine',views_m.payingfine,name = 'payingfine'),
    path('clearfine',views_m.clearfine,name = 'clearfine'),
    path('hold',views_m.hold,name = 'hold'),
    path('holdfill',views_m.holdfill,name = 'holdfill'),
    path('log',views_m.log,name = 'log',),
    path('email_all', views_r.email_all, name = 'email_all')
]
