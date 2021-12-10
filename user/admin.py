from django.contrib import admin
from django.contrib.auth.models import Permission
from user.models import UserInType, TypeUser
# Register your models here.

class TypeUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']

class UserInTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'Typeuser_id']


admin.site.register(Permission)
admin.site.register(TypeUser, TypeUserAdmin)
admin.site.register(UserInType, UserInTypeAdmin)