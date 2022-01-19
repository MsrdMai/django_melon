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
    path('productlist/', views.productlist, name='productlist'),
]