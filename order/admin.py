from django.contrib import admin
from order.models import Order, State, OrderCarving, Payment, Disease, Bug, Record, CovertImage, CancelOrder, Portage, Review, Message
# Register your models here.

class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'state_name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id_id', 'date_time', 'total_price', 'amount','shipping_cost','State_id_id','address','tel','User_id']

class OrderCarvingAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_id', 'image', 'carving_description']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_id', 'payment_image', 'bank_name']

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'disease_name','disease_description']

class BugAdmin(admin.ModelAdmin):
    list_display = ['id', 'bug_name','bug_description']

class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_id', 'recode_date', 'recode_description','recode_image','recode_weight','sweetness','quality_id_id']

class CovertImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'covert_image', 'recode_id_id']

class CancelOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_id', 'cancel_description', 'refund_contact','disease_id_id','bug_id_id']

class PortageAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_id', 'portage_name', 'portage_number','date_send']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_id', 'review_description', 'review_image','review_rating','date_send']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_id', 'content', 'date_added','User_id']
    
admin.site.register(State, StateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderCarving, OrderCarvingAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Bug, BugAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(CovertImage, CovertImageAdmin)
admin.site.register(CancelOrder, CancelOrderAdmin)
admin.site.register(Portage, PortageAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Message, MessageAdmin)