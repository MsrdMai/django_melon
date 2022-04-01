from django.contrib import admin
from django.contrib.auth.models import Permission
from store.models import Store, TypeeOrder, Quality, Product
# Register your models here.

class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'store_name', 'store_logo', 'store_img','store_address','store_description','store_phone','bank_account','name_bank','bank_id']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'store_id_id', 'product_name', 'melon_color', 'product_description','product_price','product_weight','product_amount','range','product_image','date_create',
    'date_expire','date_harvest','shipping_cost','select_carving','cost_carving','type_id_id','quality_id_id']

class TypeeOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class QualityAdmin(admin.ModelAdmin):
    list_display = ['id', 'quality_name', 'quality_description']

admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(TypeeOrder, TypeeOrderAdmin)