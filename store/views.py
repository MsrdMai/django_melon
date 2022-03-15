from email import message
from django.shortcuts import render, redirect
from user.models import TypeUser, UserInType
from order.models import State, Order, Review
from .models import Store, TypeeOrder, Quality, Product
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Max

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
        if (len(store_description) > 255) or len(store_description) <= 0:
            error_description = 'รายละเอียดร้านค้าต้องไม่เกิน 255 ตัวอักษรและมากกว่า 0 ตัวอักษร'
            count_error += 1
        if (len(store_address) > 255) or len(store_address) <= 0:
            error_address = 'รายละเอียดร้านค้าต้องไม่เกิน 255 ตัวอักษรและมากกว่า 0 ตัวอักษร'
            count_error += 1
        if len(store_phone) > 10 or len(store_phone) < 10 or len(store_phone) <= 0 or store_phone.isnumeric() == False:
            error_phone = 'หมายเลขโทรศัพท์ต้องมี 10 หลัก'
            count_error += 1   
        if len(bank_account) > 30 or len(bank_account) <= 5:
            error_account= 'ชื่อบัญชีต้องไม่เกิน 30 ตัวอักษรและมากกว่า 5 ตัวอักษร'
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
def my_store(request):
    user = request.user
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
def product_store(request):
    user = request.user
    myStore =  Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore)
    totel_product = len(totel_product)
    type_product = TypeeOrder.objects.all()  

    search_txt = request.GET.get('inputSearch', '')
    print(search_txt)
    input_Typeproduct = request.GET.get('input_Typeproduct', '')


    object_list = Product.objects.filter(
        product_name__icontains=search_txt,
        store_id = myStore,
    )
   
    if input_Typeproduct:
        object_list = object_list.filter(type_id=input_Typeproduct)

    object_list = object_list.order_by('-range')

    outofstock = []
    for i in object_list:
        if i.product_amount == 0:
            outofstock.append(i.id)

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'type_product' :type_product,
        'object_list' : object_list,
        'outofstock' : outofstock,}
    return render(request, template_name='product_store.html', context=context)


@login_required
def product_description(request, id):
    # tabfarmer
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore)
    totel_product = len(totel_product)

    # product_description
    product_des = Product.objects.get(id=id)

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'product_des' : product_des
        }
    return render(request, template_name='product_description.html', context=context)






@login_required
def edit_store(request, id):
    myStore = Store.objects.get(user_id=id)

    if request.method == 'POST':
        countedit = 0
        if (myStore.store_name != request.POST.get('store_name')):
            myStore.store_name = request.POST.get('store_name')
            countedit += 1
        if (myStore.store_description != request.POST.get('store_description')):
            myStore.store_description = request.POST.get('store_description')
            countedit += 1
        if (myStore.store_address != request.POST.get('store_address')):
            myStore.store_address = request.POST.get('store_address')
            countedit += 1
        if (myStore.store_phone != request.POST.get('store_phone')):
            myStore.store_phone = request.POST.get('store_phone')
            countedit += 1
        if (myStore.bank_account != request.POST.get('bank_account')):
            myStore.bank_account = request.POST.get('bank_account')
            countedit += 1
        if (myStore.name_bank != request.POST.get('name_bank')):
            myStore.name_bank = request.POST.get('name_bank')
            countedit += 1
        if (myStore.bank_id != request.POST.get('bank_id')):
            myStore.bank_id = request.POST.get('bank_id')
            countedit += 1

        if(myStore.latitude == None):
            countedit += 0
        if(myStore.longitude == None):
            countedit += 0

        if (myStore.latitude != request.POST.get('latitude')):
            myStore.latitude = request.POST.get('latitude')
            countedit += 1
        if (myStore.longitude != request.POST.get('longitude')):
            myStore.longitude = request.POST.get('longitude')
            countedit += 1
        
        if(request.FILES.get('store_img') == None):
            countedit += 0
        if(request.FILES.get('store_logo') == None):
            countedit += 0

        if (request.FILES.get('store_img') != None):
            myStore.store_img = request.FILES.get('store_img')
            countedit += 1
        if (request.FILES.get('store_logo') != None):
            myStore.store_logo = request.FILES.get('store_logo')
            countedit += 1
            
        if countedit == 0:
            messageEdit = "ไม่มีการแก้ไขข้อมูล"
            context = {'myStore' : myStore, 'messageEdit': messageEdit,}
            return render(request, template_name='edit_store.html', context=context)

        myStore.save()
        successfulEdit = 'แก้ไขข้อมูลฟาร์มสำเร็จ'
        context = {'myStore' : myStore,
        'successfulEdit': successfulEdit}
        return render(request, template_name='edit_store.html', context=context)
    
    context = {'myStore' : myStore,}
    return render(request, template_name='edit_store.html', context=context)
    


@login_required
def create_product(request):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore)
    totel_product = len(totel_product)
    quality_list = Quality.objects.all()
    type_list = TypeeOrder.objects.all()
    range_product = Product.objects.all().count()

    if request.method == 'POST':
        counterror = 0
        product_name = request.POST.get('product_name')
        product_img = request.FILES.get('product_img')
        melon_color = request.POST.get('melon_color')
        product_price = request.POST.get('product_price')
        product_weight = request.POST.get('product_weight')
        product_amount = request.POST.get('product_amount')
        quality_id = request.POST.get('quality_id')
        product_description = request.POST.get('product_description')
        shipping_cost = request.POST.get('shipping_cost')
        date_expire = request.POST.get('date_expire')
        date_harvest = request.POST.get('date_harvest')
        plant_place = request.POST.get('plant_place')
        water_source = request.POST.get('water_source')
        type_id = request.POST.get('type_id')

        if (request.FILES.get('product_img') == None):
            counterror += 1
            checkImg = 'กรุณาอัปโหลดรูปภาพสินค้า !'
            context = {'myStore' : myStore,
                'totel_product' : totel_product,
                'quality_list' :quality_list,
                'type_list' : type_list,
                'checkImg' : checkImg
                }
            return render(request, template_name='create_product.html', context=context)

        if (date_expire < date_harvest):
            counterror += 1
            checkd = 'วันที่เก็บเกี่ยวไม่สามารถเลือกก่อนวันที่หมดอายุได้ !'
            context = {'myStore' : myStore,
                'totel_product' : totel_product,
                'quality_list' :quality_list,
                'type_list' : type_list,
                'checkd' : checkd
                }
            return render(request, template_name='create_product.html', context=context)

        if ((product_weight.replace('.','',1).isdigit()) != True ):
            counterror += 1
            checkw = 'กรุณาใส่เป็นตัวเลขหรือเลขทศนิยม'
            context = {'myStore' : myStore,
                'totel_product' : totel_product,
                'quality_list' :quality_list,
                'type_list' : type_list,
                'checkw' : checkw
                }
            return render(request, template_name='create_product.html', context=context)

        if (type_id == None):
            counterror += 1
            checkType = 'กรุณาเลือกประเภทสินค้า !'
            context = {'myStore' : myStore,
                'totel_product' : totel_product,
                'quality_list' :quality_list,
                'type_list' : type_list,
                'checkType' : checkType
                }
            return render(request, template_name='create_product.html', context=context)

        if (type_id == '2'):
            if (request.POST.get('select_carving') == None):
                counterror += 1
                checkSelect = 'กรุณาเลือกการแกะสลักลาย !'
                context = {'myStore' : myStore,
                    'totel_product' : totel_product,
                    'quality_list' :quality_list,
                    'type_list' : type_list,
                    'checkSelect' : checkSelect
                    }
                return render(request, template_name='create_product.html', context=context)
            if (request.POST.get('cost_carving') == None):
                counterror += 1
                checkCarving = 'กรุณาระบุราคาค่าแกะสลักลาย !'
                context = {'myStore' : myStore,
                    'totel_product' : totel_product,
                    'quality_list' :quality_list,
                    'type_list' : type_list,
                    'checkCarving' : checkCarving
                    }
                return render(request, template_name='create_product.html', context=context)
            else:
                select_carving = request.POST.get('select_carving')
                cost_carving = request.POST.get('cost_carving')
                
        if (type_id == '1'):
            select_carving = 0
            cost_carving = 0


        if (counterror == 0):
            if (range_product == 0):
                range_pd = 1
                type_order = TypeeOrder.objects.get(id=type_id)
                quality = Quality.objects.get(id=quality_id)

                product_new = Product.objects.create(store_id=myStore,range=range_pd,product_name=product_name,
                product_image=product_img,
                melon_color=melon_color,product_price=product_price,product_weight=product_weight,product_amount=product_amount,
                quality_id=quality,product_description=product_description,shipping_cost=shipping_cost,plant_place=plant_place,
                date_harvest=date_harvest,date_expire=date_expire,water_source=water_source,type_id=type_order,
                select_carving=select_carving,cost_carving=cost_carving)
                product_new.save()
                successful_NewProduct = 'สร้างข้อมูลสินค้าสำเร็จ'
                context = {'myStore' : myStore,
                'totel_product' : totel_product,
                'quality_list' :quality_list,
                'type_list' : type_list,
                'successful_NewProduct' : successful_NewProduct,
                }
                return render(request, template_name='create_product.html', context=context)

            if (range_product > 0):
                type_order = TypeeOrder.objects.get(id=type_id)
                quality = Quality.objects.get(id=quality_id)
                range_pd = Product.objects.all().aggregate(Max('range')).get('range__max')
                range_pd += 1
                product_new = Product.objects.create(store_id=myStore,range=range_pd,product_name=product_name,
                product_image=product_img,
                melon_color=melon_color,product_price=product_price,product_weight=product_weight,product_amount=product_amount,
                quality_id=quality,product_description=product_description,shipping_cost=shipping_cost,plant_place=plant_place,
                date_harvest=date_harvest,date_expire=date_expire,water_source=water_source,type_id=type_order,
                select_carving=select_carving,cost_carving=cost_carving)
                product_new.save()
                successful_NewProduct = 'สร้างข้อมูลสินค้าสำเร็จ'
                context = {'myStore' : myStore,
                'totel_product' : totel_product,
                'quality_list' :quality_list,
                'type_list' : type_list,
                'successful_NewProduct' : successful_NewProduct,
                }
                return render(request, template_name='create_product.html', context=context)

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'quality_list' :quality_list,
        'type_list' : type_list,
        }
    return render(request, template_name='create_product.html', context=context)


@login_required
def order_farm(request):
    user = request.user
    myStore =  Store.objects.get(user_id=user.id)
    totel_product = Product.objects.filter(store_id=myStore)
    totel_product = len(totel_product)
    type_product = TypeeOrder.objects.all()


    search_txt = request.GET.get('inputSearch', '')
    print(search_txt)
    input_Typeproduct = request.GET.get('input_Typeproduct', '')


    object_list = Product.objects.filter(
        product_name__icontains=search_txt,
        store_id = myStore,
    )
   
    if input_Typeproduct:
        object_list = object_list.filter(type_id=input_Typeproduct)
    
    object_list = object_list.order_by('-range')
    outofstock = []
    for i in object_list:
        if i.product_amount == 0:
            outofstock.append(i.id)



    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'type_product' :type_product,
        'object_list': object_list,
        'outofstock': outofstock}
    return render(request, template_name='order_farm.html', context=context)


@login_required
def product_promote(request, id):
    # product_promote
    product = Product.objects.get(id=id)
    range_pd = Product.objects.all().aggregate(Max('range')).get('range__max')
    value = range_pd
    value = value + 1
    product.range = value
    product.save()
    text_promote = 'สินค้าของคุณได้ทำการโปรโมท อยู่ในอันดับล่าสุดแล้ว'

    context = {
        'text_promote' : text_promote,
        }
    return render(request, template_name='index.html', context=context)


@login_required
def product_close(request, id):
    # product_promote
    product = Product.objects.get(id=id)
    product.product_amount = 0
    product.save()
    text_close = 'สินค้าของคุณได้ทำการปิดการขายเรียบร้อยแล้ว'

    context = {
        'text_close' : text_close,
        }
    return render(request, template_name='index.html', context=context)



@login_required
def review_farm(request):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore)
    totel_product = len(totel_product)
    list_review = Review.objects.all()
    list_order = Order.objects.all()
    list_product = Product.objects.filter(store_id=myStore)

    zero = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0

    for order in list_order: 
        for review in list_review:
            if review.order_id.id == order.id:
                for product in list_product:
                    if order.product_id.id == product.id:
                        if review.review_rating == 1:
                            one += 1
                        elif review.review_rating == 2:
                            two += 1
                        elif review.review_rating == 3:
                            three += 1
                        elif review.review_rating == 4:
                            four += 1
                        elif review.review_rating == 5:
                            five += 1
                        else:
                            zero += 1
                        
    yValues = [five, four, three, two, one, zero]

    
    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'list_review' : list_review,
        'list_order' : list_order,
        'list_product' : list_product,
        'yValues' : yValues,
        }
    return render(request, template_name='review_farm.html', context=context)

