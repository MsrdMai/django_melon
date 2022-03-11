from email import message
from django.shortcuts import render, redirect, get_object_or_404
from user.models import TypeUser, UserInType
from .models import State, Order, Review, Message, Disease, Bug, OrderCarving, Payment, CancelOrder, Portage
from store.models import Store, TypeeOrder, Quality, Product
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf 
from django.template.loader import render_to_string
from django.urls import reverse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from .utils import get_filtered_image


class GeneratePdf(View):
    def get(self, request, id, *args, **kwargs):
        product = Product.objects.get(id=id)
        user = request.user
        today = datetime.date.today()
        open('templates/temp.html', "w", encoding='UTF-8').write(render_to_string('waybill.html', 
        {'product': product,
         'user' : user,
         'today': today,}
        ))
        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

# Create your views here.
@login_required
def chatroom(request, id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore.id)
    totel_product = len(totel_product)

    message = Message.objects.filter(order_id=id)
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        content = request.POST.get('content')
        myChat = Message.objects.create(order_id=order, content=content,User_id=user)
        myChat.save()
        return redirect('chatroom', id=order.id)

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'order' : order,
        'message' : message,
        }

    return render(request, template_name='chatroom.html', context=context)

@login_required
def order_list(request, id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore.id)
    totel_product = len(totel_product)
    type_state = State.objects.all()
    product_order = Product.objects.get(id=id)
    bug = Bug.objects.all()
    disease = Disease.objects.all()

    input_Typestate = request.GET.get('input_Typestate', '')
    order_list = Order.objects.filter(
        product_id=product_order
    )
   
    if input_Typestate:
        order_list = order_list.filter(State_id=input_Typestate)

    order_carving = OrderCarving.objects.all()
    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'product_order' : product_order,
        'type_state' :type_state,
        'bug' : bug,
        'disease' : disease,
        'order_list' : order_list,
        'order_carving' : order_carving,
        }

    return render(request, template_name='order_list.html', context=context)

@login_required
def payment_order(request,id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore.id)
    totel_product = len(totel_product)

    order = Order.objects.get(id=id)
    payment = Payment.objects.get(order_id=order)

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'order' : order,
        'payment' : payment

       }
    return render(request, template_name='payment_order.html', context=context)


@login_required
def check_payment(request, id):
    order = Order.objects.get(id=id)
    state = State.objects.get(id=3)
    order.State_id = state
    order.save()

    return redirect('order_list', id=order.product_id.id)


@login_required
def report_order(request, id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore.id)
    totel_product = len(totel_product)
    quality_list = Quality.objects.all()

    order = Order.objects.get(id=id)
    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'quality_list' :quality_list,
        'order' : order,
        
       }
    return render(request, template_name='report_order.html', context=context)


@login_required
def order_product(request, id):
    product = Product.objects.get(id=id)
    state = State.objects.get(id=1)
    user = request.user
    amount = request.POST.get('amount')
    amount = int(amount)
    address = request.POST.get('address')
    tel = request.POST.get('tel')

    if product.type_id_id == 2 and product.select_carving == 1:
        carving_img = request.FILES.get('carving_img')
        description = request.POST.get('carving_description')

        if carving_img == None:
            error_img = 'กรุณาสั่งซื้อใหม่ เนื่องจากไม่มีข้อมูลรูปภาพที่ต้องการแกะลาย'
            context = {'error_img' : error_img}
            return render(request, template_name='index.html', context=context)

        else:
            product.product_amount = product.product_amount - amount
            product.save()
            total_price = product.product_price + product.cost_carving
            total_shipping = product.shipping_cost * amount
            thisOrder = Order.objects.create(product_id=product, amount=amount, total_price=total_price, shipping_cost=total_shipping,
            State_id=state, address=address,tel=tel, User_id=user)
            thisOrder.save()
            thisCarving = OrderCarving.objects.create(order_id=thisOrder, image=carving_img,carving_description=description)
            thisCarving.save()
            order_complete_1 = 'ขอบคุณที่สั่งซื้อสินค้าของฟาร์มเรา'
            order_complete_2 = 'สามารถตรวจสอบสถานะได้ที่ คำสั่งซื้อของฉัน'
            context = {'order_complete_1' : order_complete_1, 'order_complete_2' : order_complete_2}
            return render(request, template_name='index.html', context=context)

    else:
        product.product_amount = product.product_amount - amount
        product.save()
        total_price = (product.product_price * amount)
        total_shipping = (product.shipping_cost * amount)
        thisOrder = Order.objects.create(product_id=product, amount=amount, total_price=total_price, shipping_cost=total_shipping,
        State_id=state, address=address,tel=tel, User_id=user)
        thisOrder.save()
        order_complete_1 = 'ขอบคุณที่สั่งซื้อสินค้าของฟาร์มเรา'
        order_complete_2 = 'สามารถตรวจสอบสถานะได้ที่ คำสั่งซื้อของฉัน'
        context = {'order_complete_1' : order_complete_1, 'order_complete_2' : order_complete_2}
        return render(request, template_name='index.html', context=context)


@login_required
def send_payment(request, id):
    order = Order.objects.get(id=id)
    payment_image = request.FILES.get('payment_image')
    bank_name = request.POST.get('name_bank')
    state = State.objects.get(id=2)

    if payment_image == None:
        send_payment_error = 'กรุณาอัปโหลดรูปหลักฐานการโอนเงิน'
        return redirect('orderstatus')
    else:
        order.State_id = state
        order.save()
        payment = Payment.objects.create(order_id=order, payment_image=payment_image, bank_name=bank_name)
        payment.save()

    return redirect('orderstatus')

@login_required
def cancel_order(request, id):
    order = Order.objects.get(id=id)
    cancel_description = request.POST.get('cancel_description')
    refund_contact = request.POST.get('refund_contact')
    state = State.objects.get(id=7)
    order.State_id = state

    product = Product.objects.get(id=order.product_id_id)
    product.product_amount = product.product_amount + order.amount
    product.save()
    order.save()

    disease_id = Disease.objects.get(id=6)
    bug_id = Bug.objects.get(id=5)
    mycancel = CancelOrder.objects.create(order_id=order,cancel_description=cancel_description, refund_contact=refund_contact,disease_id=disease_id,bug_id=bug_id)
    mycancel.save()
    return redirect('orderstatus')

@login_required
def farmer_cancel(request, id):
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        cancel_description = request.POST.get('cancel_description')
        refund_contact = request.POST.get('refund_contact')
        state = State.objects.get(id=6)
        order.State_id = state
        product = Product.objects.get(id=order.product_id_id)
        product.product_amount = product.product_amount + order.amount
        product.save()
        order.save()

        disease_id = Disease.objects.get(id=request.POST.get('disease_id'))
        bug_id = Bug.objects.get(id=request.POST.get('bug_id'))
        mycancel = CancelOrder.objects.create(order_id=order,cancel_description=cancel_description, refund_contact=refund_contact,disease_id=disease_id,bug_id=bug_id)
        mycancel.save()
        return redirect('order_list', id=order.product_id.id)
    else:
        return redirect('order_list', id=order.product_id.id)


@login_required
def farm_refun(request, id):
    order = Order.objects.get(id=id)
    state = State.objects.get(id=7)
    order.State_id = state
    order.save()
    return redirect('orderstatus')

@login_required
def send_portage(request, id):
    order = Order.objects.get(id=id)
    state = State.objects.get(id=4)
    order.State_id = state
    order.save()
    portage_name = request.POST.get('portage_name')
    portage_number = request.POST.get('portage_number')
    my_portage = Portage.objects.create(order_id=order, portage_name=portage_name, portage_number=portage_number)
    my_portage.save()
    return redirect('order_list', id=order.product_id.id)

@login_required
def confirmorder(request, id):
    order = Order.objects.get(id=id)
    state = State.objects.get(id=5)
    order.State_id = state
    order.save()
    return redirect('orderstatus')
    
