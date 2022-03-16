from django.contrib import auth
from django.urls import path,include
from . import views
from .views import GeneratePdf

urlpatterns = [
    path('order_product/<int:id>/', views.order_product, name='order_product'),
    path('send_payment/<int:id>/', views.send_payment, name='send_payment'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),
    path('order_list/<int:id>/', views.order_list, name='order_list'),
    path('payment_order/<int:id>/', views.payment_order, name='payment_order'),
    path('check_payment/<int:id>/', views.check_payment, name='check_payment'),   
    path('farmer_cancel/<int:id>/', views.farmer_cancel, name='farmer_cancel'),   
    path('farm_refun/<int:id>/', views.farm_refun, name='farm_refun'),   
    path('send_portage/<int:id>/', views.send_portage, name='send_portage'), 
    path('confirmorder/<int:id>/', views.confirmorder, name='confirmorder'),               
    path('report_order/<int:id>/', views.report_order, name='report_order'),
    path('covert_image/<int:id>/', views.covert_image, name='covert_image'),    
    path('chatroom/<int:id>/', views.chatroom, name='chatroom'),
    path('pdf/<int:id>/', GeneratePdf.as_view(), name="orderPdf"),
    path('send_review/<int:id>/', views.send_review, name="send_review"),

]