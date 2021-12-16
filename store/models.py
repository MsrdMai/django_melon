from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Store(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=30)
    store_logo = models.ImageField(upload_to='store_logo/', null=True)
    store_img = models.ImageField(upload_to='store_img/', null=True)
    store_address = models.CharField(max_length=255)
    store_description = models.CharField(max_length=255)
    store_phone = models.CharField(max_length=10)
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    bank_account = models.CharField(max_length=30)
    bank_id = models.CharField(max_length=13)
    name_bank = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = "Store"

class TypeeOrder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    class Meta:
        managed = True
        db_table = "TypeeOrder"

class Quality(models.Model):
    id = models.AutoField(primary_key=True)
    quality_name = models.CharField(max_length=30)
    quality_description = models.CharField(max_length=255)
    class Meta:
        managed = True
        db_table = "Quality"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=20)
    melon_color = models.CharField(max_length=10)    
    product_description = models.CharField(max_length=255)   
    product_price = models.IntegerField()
    product_amount = models.IntegerField()
    range = models.IntegerField()
    product_image = models.ImageField(upload_to='product_image/', null=True)
    date_create = models.DateTimeField(auto_now=True)
    date_plant = models.DateField(null=True)
    date_harvest = models.DateField(null=True)
    plant_place = models.CharField(max_length=20)
    water_source = models.CharField(max_length=20)
    shipping_cost = models.IntegerField()
    select_carving = models.BooleanField()
    cost_carving = models.IntegerField()
    type_id = models.ForeignKey(TypeeOrder, on_delete=models.CASCADE)
    quality_id = models.ForeignKey(Quality, on_delete=models.CASCADE)
    
    class Meta:
        managed = True
        db_table = "Product"

