from django.contrib import auth
from django.urls import path,include
from . import views
from .views import GeneratePdf


urlpatterns = [
    path('chatroom/<int:id>/', views.chatroom, name='chatroom'),
    path('pdf/', GeneratePdf.as_view()), 
    # path('pdf/<pk>', GeneratePdf.as_view(), name="orderPdf"), 

]