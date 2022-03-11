from django.db import models
from django.contrib.auth.models import User
from store.models import Product, Quality
from user.models import TypeUser,UserInType

# Create your models here.

class State(models.Model):
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=30)
    class Meta:
        managed = True
        db_table = "State"

    # STATUS = (
    #     (รอชำระเงิน, 'Waiting for payment'),
    #     (รอการตรวจสอบจากร้านค้า, 'Waiting for verify'),
    #     (เตรียมคำสั่งซ้ือ, '‘Prepare order'),
    #     (ร้านค้าส่งสินค้าแล้ว, 'Product delivered'),
    #     (ได้รับสินค้าแล้ว, 'Received the product'),
    #     (รอการรีวิว, 'Waiting for review'),
    #     (คำสั่งซื้อเสร็จสมบูรณ์, '‘Complete order'),
    #     (แจ้งยกเลิกคำสั่งซื้อ รอยืนยันจากผู้ซ้ื้อ, 'Notify cancel order'),
    #     (ยกเลิกคe สั่งซื้อแล้ว, '‘Canceled order'),

    # )

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)  
    total_price = models.IntegerField()
    amount = models.IntegerField()
    shipping_cost = models.IntegerField()
    State_id = models.ForeignKey(State, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    tel = models.CharField(max_length=10)
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = "Order"

class OrderCarving(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img_Ordercarving/', null=True)
    carving_description = models.CharField(max_length=255)
    class Meta:
        managed = True
        db_table = "OrderCarving"

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_image = models.ImageField(upload_to='payment_image/', null=False)
    bank_name = models.CharField(max_length=100)
    class Meta:
        managed = True
        db_table = "Payment"

class Disease(models.Model):
    id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=50)
    disease_description = models.CharField(max_length=255)
    class Meta:
        managed = True
        db_table = "Disease"

class Bug(models.Model):
    id = models.AutoField(primary_key=True)
    bug_name = models.CharField(max_length=50)
    bug_description = models.CharField(max_length=255)
    class Meta:
        managed = True
        db_table = "Bug"

class Record(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    recode_date = models.DateTimeField(auto_now=True)  
    recode_description = models.CharField(max_length=255)
    recode_image = models.ImageField(upload_to='recode_image/', null=False)
    recode_weight  = models.FloatField()
    sweetness = models.FloatField()
    quality_id = models.ForeignKey(Quality, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = "Record"

class CovertImage(models.Model):
    id = models.AutoField(primary_key=True)
    covert_image = models.ImageField(upload_to='covert_image/', null=True)
    recode_id = models.ForeignKey(Record, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "CovertImage"


class CancelOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    cancel_description = models.CharField(max_length=255)
    refund_contact = models.CharField(max_length=255)
    disease_id = models.ForeignKey(Disease, on_delete=models.CASCADE)
    bug_id= models.ForeignKey(Bug, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = "CancelOrder"

class Portage(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    portage_name = models.CharField(max_length=255)
    portage_number = models.CharField(max_length=20)
    date_send = models.DateTimeField(auto_now=True)  
    class Meta:
        managed = True
        db_table = "Portage"
     
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    review_description = models.CharField(max_length=255)
    review_image = models.ImageField(upload_to='reviews/', null=False)
    review_rating = models.IntegerField()
    date_send = models.DateTimeField(auto_now=True)  
    class Meta:
        managed = True
        db_table = "Review"

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = "Message"