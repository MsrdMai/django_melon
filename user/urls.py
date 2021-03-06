from django.contrib import auth
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index_page, name='index'),
    path('login_page/', views.login_page, name='login_page'),
    path('register_type/', views.register_type, name='register_type'),
    path('logout/', views.logout_page, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('product_buy/', views.product_buy, name='product_buy'),
    path('product_book/', views.product_book, name='product_book'),
    path('orderstatus/', views.orderstatus, name='orderstatus'),
    path('product_desc/<int:id>/', views.product_desc, name='product_desc'),
    path('product_total/', views.product_total, name='product_total'),
    path('farm-detail/<int:id>/', views.farm_detail, name='farm-detail'),    
    path('review_detail/<int:id>/', views.review_detail, name='review_detail'),
    path('chatTofarmer/<int:id>/', views.chatTofarmer, name='chatTofarmer'),      
    path('send_message_toFarm/<int:id>/', views.message_toFarm, name='message_toFarm'),
    path('getMessages_fromFarm/<int:id>/', views.messages_fromFarm, name='messages_fromFarm'),          
    path('admin_manager/', views.admin_manager, name='admin_manager'), 
    path('admin_customer/', views.admin_customer, name='admin_customer'),
    path('admin_editOrder/', views.admin_editOrder, name='admin_editOrder'), 
    path('delete_customer/<int:id>/', views.delete_customer, name='delete_customer'),
    path('historyorder/', views.historyorder, name='historyorder'),    
]