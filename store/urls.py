from django.contrib import auth
from django.urls import path,include
from . import views

urlpatterns = [
    path('create_store/', views.create_store, name='create_store'),
    path('my_store/', views.my_store, name='my_store'),
    path('product_description/<int:id>/', views.product_description, name='product_description'),
    path('product_promote/<int:id>/', views.product_promote, name='product_promote'),
    path('product_close/<int:id>/', views.product_close, name='product_close'),    
    path('product_store/', views.product_store, name='product_store'),
    path('create_product/', views.create_product, name='create_product'),
    path('edit_store/<int:id>/', views.edit_store, name='edit_store'),
    path('order_farm/', views.order_farm, name='order_farm'),
    path('order_list/<int:id>/', views.order_list, name='order_list'),
    path('review_farm/', views.review_farm, name='review_farm'),

]