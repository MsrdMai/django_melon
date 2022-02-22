from django.contrib import auth
from django.urls import path,include
from . import views
from .views import GeneratePdf


urlpatterns = [
    path('order_list/<int:id>/', views.order_list, name='order_list'),
    path('payment_order/', views.payment_order, name='payment_order'),
    path('report_order/', views.report_order, name='report_order'),
    path('chatroom/<int:id>/', views.chatroom, name='chatroom'),
    path('pdf/<int:id>/', GeneratePdf.as_view(), name="orderPdf"), 

]