from django.contrib import admin
from django.contrib.auth.models import Permission
from store.models import Store, TypeeOrder, Quality, Product
# Register your models here.

class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'store_name', 'store_logo', 'store_img',]


admin.site.register(Store, StoreAdmin)
