from django.contrib import auth
from django.urls import path,include
from . import views


urlpatterns = [
    path('chatroom/<int:id>/', views.chatroom, name='chatroom'),
  


]