from django.shortcuts import render, redirect
from user.models import TypeUser, UserInType
from order.models import State, Order, Review
from .models import Store, TypeeOrder, Quality, Product
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
# from .models import 
# Create your views here.

@login_required
def create_store(request):
    user = request.user
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        store_description = request.POST.get('store_description')
        store_address = request.POST.get('store_address')
        store_phone = request.POST.get('store_phone')
        bank_account = request.POST.get('bank_account')
        name_bank = request.POST.get('name_bank')
        bank_id = request.POST.get('bank_id')
        store_img = request.FILES.get('store_img')
        store_logo = request.FILES.get('store_logo')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        count_error  = 0
        error_bankid = ''
        error_storename = ''
        error_description = ''
        error_address = ''
        error_phone = ''
        error_latitude = ''
        error_account = ''
        error_namebank = ''
        error_logo = ''
        error_img = ''


        if len(bank_id) > 13 or len(bank_id) < 10 or len(bank_id) == 12 or len(bank_id) <= 0:
            error_bankid = 'หมายเลขบัญชีต้องเป็น 10 หรือ 13 หลัก'
            count_error += 1
        if len(store_name) > 30 or len(store_name) <= 0:
            error_storename = 'ชื่อร้านค้าต้องไม่เกิน 30 ตัวอักษร'
            count_error += 1
        if len(store_description) > 255 or len(store_description) <= 0:
            error_description = 'รายละเอียดร้านค้าต้องไม่เกิน 100 ตัวอักษร'
            count_error += 1
        if len(store_address) > 255 or len(store_address) <= 0:
            error_address = 'รายละเอียดร้านค้าต้องไม่เกิน 100 ตัวอักษร'
            count_error += 1
        if len(store_phone) > 10 or len(store_phone) < 10 or len(store_phone) <= 0 or store_phone.isnumeric() == False:
            error_phone = 'หมายเลขโทรศัพท์ต้องมี 10 หลัก'
            count_error += 1   
        if len(bank_account) > 30 or len(bank_account) <= 5:
            error_account= 'ชื่อบัญชีต้องไม่เกิน 30 ตัวอักษร'
            count_error += 1        
        if name_bank == '0':
            error_namebank = 'โปรดระบุชื่อธนาคาร'
            count_error += 1           
        if store_logo == None:
            error_logo = 'โปรดอัปโหลดรูปโลโก้ฟาร์ม'
            count_error += 1          
        if store_img == None:
            error_img = 'โปรดอัปโหลดรูปภาพบรรยากาศฟาร์ม'
            count_error += 1   
        if latitude == None or longitude == None:
            error_latitude = 'กรุณาระบุตำแหน่งฟาร์ม'
            count_error += 1        

        if  count_error > 0:     
            context = {
            'error_bankid': error_bankid,
            'error_storename': error_storename,
            'error_description': error_description,
            'error_address': error_address,
            'error_phone': error_phone,
            'error_latitude': error_latitude,
            'error_account': error_account,
            'error_namebank': error_namebank,
            'error_logo' : error_logo,
            'error_img' : error_img,
            }
            return render(request, template_name='create_store.html', context=context)

        else:
            my_store = Store.objects.create(
                user_id=user,
                store_name=store_name,
                store_description=store_description,
                store_address=store_address,
                store_phone=store_phone,
                bank_account=bank_account,
                name_bank=name_bank,
                bank_id=bank_id,
                store_img=store_img,
                store_logo=store_logo,
                latitude=latitude,
                longitude=longitude)
            my_store.save()
            successfulFarm = 'สร้างข้อมูลฟาร์มสำเร็จ'
            context = {'successfulFarm': successfulFarm,}
            return render(request, template_name='index.html', context=context)
    return render(request, template_name='create_store.html')

@login_required
def my_store(request, id):
    user = User.objects.get(pk=id)
    checkStore = Store.objects.filter(user_id=user)
    checkStore = len(checkStore)
    context = {}
    if checkStore == 0:  
        return redirect(to='create_store')
    else:
        myStore = Store.objects.get(user_id=user)
        totel_product = Product.objects.filter(store_id=myStore)
        totel_product = len(totel_product)
        latitude = myStore.latitude
        longitude = myStore.longitude
        context = {'myStore' : myStore,
        'latitude' : latitude,
        'longitude' : longitude,
        'totel_product' : totel_product,
        }
    
    return render(request, template_name='my_store.html', context=context)


@login_required
def product_description(request):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore)
    totel_product = len(totel_product)
    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        }
    return render(request, template_name='product_description.html', context=context)