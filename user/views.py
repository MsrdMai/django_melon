from itertools import product
from sre_parse import State
from django.shortcuts import render, redirect
from .models import TypeUser, UserInType
from order.models import State, Order, Review, Message, OrderCarving, Portage
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


def orderstatus(request):
    user = request.user
    myorder = Order.objects.filter(User_id=user)

    count_portage = 0
    portage = Portage.objects.all()

    for d in myorder:
        for p in portage:
            if d.id == p.order_id:
                count_portage += 1

    count_review = Order.objects.filter(User_id=user, State_id=5).count()
    count_waitpay = Order.objects.filter(User_id=user, State_id=1).count()
    count_prepar = Order.objects.filter(User_id=user, State_id=3).count()

    all_carving = OrderCarving.objects.all()
    list_carving = []

    for j in myorder:
        for i in all_carving:
            if i.order_id == j.id:
                list_carving.append(i.id)

    context = {
        'myorder' : myorder,
        'list_carving' : list_carving,
        'count_portage' : count_portage,
        'count_review' : count_review,
        'count_waitpay' : count_waitpay,
        'count_prepar' : count_prepar,

    }

    return render(request, template_name='orderstatus.html', context=context)

def product_desc(request,id):
    data_product = Product.objects.get(id=id)
    context = {
        'data_product' : data_product
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

    context = {
        'farm_detail' : farm_detail,
        'totel_product' : totel_product,
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

    # เรียงใหม่
    sorded_qulitydict = sorted(qulitydict.items(), key=lambda x: x[1], reverse=True)
    v = []
    # จำยัดใส่ List
    for i in qulitydict:
        for values in qulitydict.values():
            v.append(values)

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
