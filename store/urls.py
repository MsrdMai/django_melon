from django.contrib import auth
from django.urls import path,include
from . import views

urlpatterns = [
    path('create_store/', views.create_store, name='create_store'),
    path('my_store/<int:id>/', views.my_store, name='my_store'),
    path('product_description/', views.product_description, name='product_description'),
    path('product_store/<int:id>/', views.product_store, name='product_store'),
    path('create_product/', views.create_product, name='create_product'),
]