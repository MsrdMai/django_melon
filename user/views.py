from itertools import product
from sre_parse import State
from django.shortcuts import render, redirect
from .models import TypeUser, UserInType
from order.models import State, Order, Review, Message, OrderCarving, Portage, CancelOrder,Record, CovertImage
from store.models import Store, TypeeOrder, Quality, Product
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, Group
from store.models import Product, Quality, Store
from order.models import Order, State 
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.db.models import Max
from django.contrib.auth.decorators import user_passes_test
import pythainlp
import datetime
from pythainlp.util import thai_strftime
# Create your views here.


def login_page(request):

    context = {}
    if request.user.is_authenticated:
       return redirect(to='index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user=user)
            return redirect('index')

        else:
            context['error'] = 'Wrong username or password!'
            return render(request, template_name='login.html', context=context)

    return render(request, template_name='login.html')


def logout_page(request):
    auth_logout(request)
    return redirect(to='index')


def register_type(request):
    if request.user.is_authenticated:
        user_id = request.user
        user_id = user_id.id
        user = User.objects.get(pk=user_id)
        userInType = UserInType.objects.filter(user_id=user)
        userInType = len(userInType)
        list_typeUser = TypeUser.objects.all()
        farmer_group = Group.objects.get(name='Farmer') 
        customer_group = Group.objects.get(name='Customer') 

        context = {}

        if userInType == 0:
            if request.method == 'POST':
                type_userSeletor = TypeUser.objects.get(id=request.POST.get('accountType'))
                new_UserInType = UserInType.objects.create(
                user_id=user,
                Typeuser_id=type_userSeletor,)
                new_UserInType.save()

                if type_userSeletor.id == 1:
                    farmer_group.user_set.add(user)
                else:
                    customer_group.user_set.add(user)

                msg = 'คุณเลือกประเภทผู้ใช้งานสำเร็จ'
                context = {'msg': msg,}
                return render(request, template_name='index.html', context=context)
            else:
                new_UserInType = UserInType.objects.none()
        else:      
            return redirect(to='index')
            
    else:
        return redirect(to='login_page')

    context = {'list_typeUser': list_typeUser, 'userInType':userInType}    

    return render(request, template_name='register.html', context=context)

def index_page(request):
    try:
        if request.user.is_authenticated:
            check_UserInType = UserInType.objects.all()
            user_id = request.user
            user_id = user_id.id
            user = User.objects.get(pk=user_id)
            userInType = UserInType.objects.filter(user_id=user)
            userInType = len(userInType)

            if request.user.is_superuser == False:
                if userInType <= 0:        
                    return redirect(to='register_type')
            else:
                return render(request, template_name='index.html')
    except IntegrityError as e:
        user_type = UserInType.objects.get(user_id=user)

    return render(request, template_name='index.html')

@login_required
def profile(request, id):
    user = User.objects.get(pk=id)
    user_info = UserInType.objects.get(user_id=user)
    context = {
        'user_info': user_info,
        'user' : user,
    }  

    return render(request, template_name='profile.html', context=context)


def product_buy(request):
    product_list = Product.objects.filter(type_id=1)
    product_list = product_list.order_by('-range')

    outofstock = []
    for i in product_list:
        if i.product_amount == 0:
            outofstock.append(i.id)

    context = {
        'product_list' : product_list,
        'outofstock' : outofstock,
    }
    return render(request, template_name='product_buy.html', context=context)

def product_book(request):
    product_list = Product.objects.filter(type_id=2)
    product_list = product_list.order_by('-range')

    outofstock = []
    for i in product_list:
        if i.product_amount == 0:
            outofstock.append(i.id)


    context = {
        'product_list' : product_list,
        'outofstock' : outofstock,
    }
    return render(request, template_name='product_book.html', context=context)

@login_required
def orderstatus(request):
    user = request.user
    myorder = Order.objects.filter(User_id=user)
    portage = Portage.objects.all()
    count_review = Order.objects.filter(User_id=user, State_id=5).count()
    count_sent = Order.objects.filter(User_id=user, State_id=4).count()
    count_waitpay = Order.objects.filter(User_id=user, State_id=1).count()
    count_prepar = Order.objects.filter(User_id=user, State_id=3).count()

    my_record = Record.objects.all()
    list_img = CovertImage.objects.all()

    # for j in myorder:
    #     for i in record:
    #         if i.order_id == j.id:
    #             my_record.append(i.id)

    # all_carving = OrderCarving.objects.all()
    # list_carving = []

    # for j in myorder:
    #     for i in all_carving:
    #         if i.order_id == j.id:
    #             list_carving.append(i.id)

    context = {
        'myorder' : myorder,
        'portage' : portage,
        'count_review' : count_review,
        'count_waitpay' : count_waitpay,
        'count_prepar' : count_prepar,
        'count_sent' : count_sent,
        'my_record' : my_record,
        'list_img' : list_img,
    }
    return render(request, template_name='orderstatus.html', context=context)


@login_required
def chatTofarmer(request,id):
    user = request.user
    message = Message.objects.filter(order_id=id)
    order = Order.objects.get(id=id)
    
    store = order.product_id.store_id

    if request.method == 'POST':
        content = request.POST.get('content')
        myChat = Message.objects.create(order_id=order, content=content,User_id=user)
        myChat.save()
        return redirect('chatTofarmer', id=order.id)

    context = {
        'message': message,
        'order' : order,
        'store' :store,
    }
    return render(request, template_name='chatTofarmer.html', context=context)

def product_desc(request,id):
    data_product = Product.objects.get(id=id)
    date_ex = data_product.date_expire
    date_har = data_product.date_harvest
    fmt = "%d %b %y"
    expire = thai_strftime(date_ex, fmt)
    harvest = thai_strftime(date_har, fmt)
    context = {
        'data_product' : data_product,
        'expire' : expire,
        'harvest' : harvest
    }
    return render(request, template_name='product_desc.html', context=context)

def product_total(request):
    return render(request, template_name='product_total.html')

def farm_detail(request,id):
    farm_detail = Store.objects.get(id=id)
    latitude = farm_detail.latitude
    longitude = farm_detail.longitude
    product_list = Product.objects.filter(store_id=farm_detail)
    totel_product = len(product_list)

    product_list = product_list.order_by('-range')
    outofstock = []
    for i in product_list:
        if i.product_amount == 0:
            outofstock.append(i.id)

    context = {
        'farm_detail' : farm_detail,
        'latitude' :latitude,
        'longitude':longitude,
        'totel_product' : totel_product,
        'product_list' :product_list,
        'outofstock' : outofstock,
    }
    return render(request, template_name='farm_detail.html', context=context)    

def review_detail(request,id):
    farm_detail = Store.objects.get(id=id)
    product_list = Product.objects.filter(store_id=farm_detail)
    totel_product = len(product_list)
    list_review = Review.objects.all()
    list_order = Order.objects.all()

    zero = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0

    for order in list_order: 
        for review in list_review:
            if review.order_id.id == order.id:
                for product in product_list:
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

    context = {
        'farm_detail' : farm_detail,
        'totel_product' : totel_product,
        'yValues' : yValues,
        'product_list' : product_list,
        'list_review' : list_review,
        'list_order' : list_order,
    }
    return render(request, template_name='review_detail.html', context=context)    


@user_passes_test(lambda s: s.is_staff)
@login_required
def admin_manager(request):
    store = Product.objects.all().values()
    df = pd.DataFrame(store)
    product_name = df.product_name.tolist()
    price = df['product_price'].tolist()
    count_product =Product.objects.all().count()
    count_user = User.objects.all().count()
    count_user = count_user - 1
    count_store = Store.objects.all().count()
    count_order  =Order.objects.all().count()
    product =Product.objects.all()
    qulity = Quality.objects.all()
    ## Product-Qulity
    q = []
    for i in qulity:
        q.append(i.quality_name)

    count_product_amont = 0
    product = Product.objects.all()
    for i in product:
        count_product_amont += i.product_amount

    qulitydict = {}

    for j in qulity:
        qulitydict[j.quality_name] = 0

    for i in product:
        for j in qulity:
            if i.quality_id_id == j.id:
                qulitydict[j.quality_name] += i.product_amount
    v = []
    # จำยัดใส่ List
    for i in qulitydict:
        for values in qulitydict.values():
            v.append(values)

    ## ## ## ## ## ## 

    max_pd = Product.objects.all().aggregate(Max('product_price')).get('product_price__max')

    context = {
        'store' : store,
        "price": price,
        "product_name" : product_name,
        'count_product' : count_product,
        'count_user' : count_user,
        'count_store' : count_store,
        'count_order' : count_order,
        'q' : q,
        'v' : v,
        'count_product_amont' : count_product_amont,
        'max_pd' : max_pd

    }

    return render(request, template_name='admin_manager.html', context=context)

@user_passes_test(lambda s: s.is_staff)
@login_required
def admin_customer(request):
    user_list = UserInType.objects.all()
    context = {
        'user_list' : user_list,
    } 
    return render(request, template_name='admin_customer.html', context=context)

@user_passes_test(lambda s: s.is_staff)
@login_required
def delete_customer(request, id):
    user = User.objects.get(id=id)
    user_list = UserInType.objects.all()

    try:
        user.delete()
        txt = 'ลบรายชื่อสำเร็จแล้ว'
    except:
        txt = 'ลบรายชื่อสำเร็จแล้ว'

    context = {
            'txt' : txt,
            'user_list' : user_list,
        }
    return render(request, template_name='admin_customer.html', context=context)
        
@user_passes_test(lambda s: s.is_staff)
@login_required
def admin_editOrder(request):
    type_state = State.objects.all()
    context = {
            'type_state' : type_state,
        }
    return render(request, template_name='admin_editOrder.html', context=context)

def historyorder(request):
    user = request.user
    myorder = Order.objects.filter(User_id=user)
    list_cancel = CancelOrder.objects.all()
    count_complete = Order.objects.filter(User_id=user, State_id=8).count()
    count_cancel = Order.objects.filter(User_id=user, State_id=7).count()
    count_refund = Order.objects.filter(User_id=user, State_id=6).count()
    
    context = {
            'myorder' : myorder,
            'list_cancel' : list_cancel,
            'count_complete': count_complete,
            'count_cancel': count_cancel,
            'count_refund' : count_refund,
        }
    return render(request, template_name='historyorder.html', context=context)