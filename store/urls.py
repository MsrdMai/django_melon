from django.contrib import auth
from django.urls import path,include
from . import views


urlpatterns = [
    path('create_store/', views.create_store, name='create_store'),
    path('my_store/<int:id>/', views.my_store, name='my_store'),


]