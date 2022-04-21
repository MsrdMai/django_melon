from django.shortcuts import render, redirect
from user.models import TypeUser, UserInType
from .models import Review, State, Order, Message, Disease, Bug, OrderCarving, Payment, CancelOrder, Portage, Record, CovertImage
from store.models import Store, Quality, Product
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf 
from django.template.loader import render_to_string
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pythainlp
import datetime
from pythainlp.util import thai_strftime
import pythainlp.util
from django.http import HttpResponse, JsonResponse

class GeneratePdf(View):
    def get(self, request, id, *args, **kwargs):
        product = Product.objects.get(id=id)
        user = request.user
        today = datetime.date.today()

        fmt = "%Aที่ %-d %B พ.ศ. %Y เวลา %H:%M น."
        date = thai_strftime(today, fmt)

        open('templates/temp.html', "w", encoding='UTF-8').write(render_to_string('waybill.html', 
        {'product': product,
         'user' : user,
         'today': today,
         'date' : date,
         }
        ))
        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')

        # rendering the template
        response = HttpResponse(pdf, content_type='application/pdf')  
        return response


# Create your views here.
# @login_required
# def chatroom(request, id):
#     user = request.user
#     myStore = Store.objects.get(user_id=user)
#     totel_product = Product.objects.filter(store_id=myStore.id)
#     totel_product = len(totel_product)

#     message = Message.objects.filter(order_id=id)
#     order = Order.objects.get(id=id)
#     customer = order.User_id

#     if request.method == 'POST':
#         content = request.POST.get('content')
#         myChat = Message.objects.create(order_id=order, content=content,User_id=user)
#         myChat.save()
#         return redirect('chatroom', id=order.id)

#     context = {'myStore' : myStore,
#         'totel_product' : totel_product,
#         'order' : order,
#         'message' : message,
#         'customer' : customer,
#         }

#     return render(request, template_name='chatroom.html', context=context)
@login_required
def chatroom(request, id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    product = Product.objects.filter(store_id=myStore)
    waitcheck_order = 0
    waitpay_order = 0
    refund_order = 0
    for p in product:
        waitcheck_order += Order.objects.filter(product_id=p.id, State_id=2).count()
        waitpay_order += Order.objects.filter(product_id=p.id, State_id=1).count()
        refund_order += Order.objects.filter(product_id=p.id, State_id=6).count()
    count_all = waitcheck_order + waitpay_order + refund_order
    totel_product = len(product)

    order = Order.objects.get(id=id)
    customer = order.User_id
    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'waitcheck_order' : waitcheck_order,
        'waitpay_order' : waitpay_order,
        'refund_order' : refund_order,
        'count_all' : count_all,
        'order' : order,
        'user' : user,
        'customer' : customer,
        }
    return render(request, template_name='chatroom.html', context=context)

@login_required
def send_message(request,id):
    user = request.user
    content = request.POST['content']
    order = Order.objects.get(id=id)
    new_message = Message.objects.create(order_id=order, content=content,User_id=user)
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required
def getMessages(request,id):
    user = request.user
    order = Order.objects.get(id=id)
    message = Message.objects.filter(order_id=order.id)
    return JsonResponse({"messages":list(message.values())})

@login_required
def order_list(request, id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    product = Product.objects.filter(store_id=myStore)
    waitcheck_order = 0
    waitpay_order = 0
    refund_order = 0
    for p in product:
        waitcheck_order += Order.objects.filter(product_id=p.id, State_id=2).count()
        waitpay_order += Order.objects.filter(product_id=p.id, State_id=1).count()
        refund_order += Order.objects.filter(product_id=p.id, State_id=6).count()
    count_all = waitcheck_order + waitpay_order + refund_order
    totel_product = len(product)
    type_state = State.objects.all()
    product_order = Product.objects.get(id=id)

    date_ex = product_order.date_expire
    date_har = product_order.date_harvest
    fmt = "%d %b %y"
    expire = thai_strftime(date_ex, fmt)
    harvest = thai_strftime(date_har, fmt)

    bug = Bug.objects.all()
    disease = Disease.objects.all()
    list_cancel = CancelOrder.objects.all()

    input_Typestate = request.GET.get('input_Typestate', '')
    order_list = Order.objects.filter(
        product_id=product_order
    )
   
    if input_Typestate:
        order_list = order_list.filter(State_id=input_Typestate)

    order_carving = OrderCarving.objects.all()
    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'waitcheck_order' : waitcheck_order,
        'waitpay_order' : waitpay_order,
        'refund_order' : refund_order,
        'count_all' : count_all,
        'product_order' : product_order,
        'type_state' :type_state,
        'bug' : bug,
        'disease' : disease,
        'order_list' : order_list,
        'order_carving' : order_carving,
        'list_cancel' : list_cancel,
        'expire' : expire,
        'harvest' : harvest
        }

    return render(request, template_name='order_list.html', context=context)

@login_required
def payment_order(request,id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    product = Product.objects.filter(store_id=myStore.id)
    waitcheck_order = 0
    waitpay_order = 0
    refund_order = 0
    for p in product:
        waitcheck_order += Order.objects.filter(product_id=p.id, State_id=2).count()
        waitpay_order += Order.objects.filter(product_id=p.id, State_id=1).count()
        refund_order += Order.objects.filter(product_id=p.id, State_id=6).count()
    count_all = waitcheck_order + waitpay_order + refund_order
    totel_product = len(product)

    order = Order.objects.get(id=id)
    payment = Payment.objects.get(order_id=order)

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'waitcheck_order' : waitcheck_order,
        'waitpay_order' : waitpay_order,
        'refund_order' : refund_order,
        'count_all' : count_all,
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
    my_record = Record.objects.filter(order_id=id)
    count_record = Record.objects.filter(order_id=id).count()
    list_img = CovertImage.objects.all()
    myStore = Store.objects.get(user_id=user)
    product = Product.objects.filter(store_id=myStore)
    waitcheck_order = 0
    waitpay_order = 0
    refund_order = 0
    for p in product:
        waitcheck_order += Order.objects.filter(product_id=p.id, State_id=2).count()
        waitpay_order += Order.objects.filter(product_id=p.id, State_id=1).count()
        refund_order += Order.objects.filter(product_id=p.id, State_id=6).count()
    count_all = waitcheck_order + waitpay_order + refund_order
    totel_product = len(product)
    quality_list = Quality.objects.all()
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        recode_description = request.POST.get('recode_description')
        recode_weight = request.POST.get('recode_weight')
        quality_id = request.POST.get('quality_id')
        sweetness = request.POST.get('sweetness')
        recode_image = request.FILES.get('recode_image')
        quality = Quality.objects.get(id=quality_id)

        if ((pythainlp.util.countthai(request.FILES.get('recode_image')) > 0) or (recode_image == None)):
            error_img = 'กรุณาอัปโหลดรูปภาพ หรือกรุณาเปลี่ยนชื่อไฟร์เป็นภาษาอังกฤษ'
            context = {'myStore' : myStore,
                'totel_product' : totel_product,
                'quality_list' :quality_list,
                'order' : order,
                'my_record' : my_record,
                'list_img' : list_img,
                'count_record' : count_record,
                'error_img' : error_img,
            }
            return render(request, template_name='report_order.html', context=context)
        else:
            new_record = Record.objects.create(order_id=order, recode_description=recode_description,recode_image=recode_image,
            recode_weight=recode_weight, sweetness=sweetness, quality_id=quality)
            new_record.save()
            covert_image = CovertImage.objects.create(recode_id=new_record, covert_image=recode_image)
            covert_image.save()
            return redirect('covert_image', id=covert_image.id)

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'waitcheck_order' : waitcheck_order,
        'waitpay_order' : waitpay_order,
        'refund_order' : refund_order,
        'count_all' : count_all,
        'quality_list' :quality_list,
        'order' : order,
        'my_record' : my_record,
        'list_img' : list_img,
        'count_record' : count_record
       }
    return render(request, template_name='report_order.html', context=context)

@login_required
def covert_image(request, id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    product = Product.objects.filter(store_id=myStore)
    waitcheck_order = 0
    waitpay_order = 0
    refund_order = 0
    for p in product:
        waitcheck_order += Order.objects.filter(product_id=p.id, State_id=2).count()
        waitpay_order += Order.objects.filter(product_id=p.id, State_id=1).count()
        refund_order += Order.objects.filter(product_id=p.id, State_id=6).count()
    count_all = waitcheck_order + waitpay_order + refund_order
    totel_product = len(product)

    get_img = CovertImage.objects.get(id=id)
    get_order = get_img.recode_id.order_id

    try:
        img_main  = cv2.imread(get_img.covert_image.path, flags=cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img_main, cv2.COLOR_BGR2GRAY)
        # To calculate the gradients of an image it is best not to use uint8 since you will miss some edges
        # Calculate gradients using the laplacian method
        # Convert the image to using 64 bit floats and calculate the gradients afterwards

        lap = cv2.Laplacian(img_gray,cv2.CV_64F)  
        lap = np.uint8(np.absolute(lap))  
        # Convert the image back into uint8
        # Calculate the edges using the Sobel method
        # In the Sobel method the gradients are calculated both horizontally and vertically
        sobel_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0)  # Remember to convert into 64 bit floats
        sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1)

        sobel_x = np.uint8(np.absolute(sobel_x))  # remember to convert back into 8 bit unsigned integers
        sobel_y = np.uint8(np.absolute(sobel_y))
        sobel_combined = cv2.bitwise_or(sobel_x, sobel_y)

        ## Save CovertImage
        cv2.imwrite(get_img.covert_image.path, sobel_combined)

        success = 'บันทึกรายงานสำเร็จ'
        context = {'get_img' : get_img,
            'get_order' : get_order,
            'myStore' : myStore,
            'totel_product' : totel_product,
            'success' : success
        }
        return render(request, template_name='covert_image.html', context=context)
    except:
        error_txt = 'มีข้อผิดพลาดในการอัปโหลดรูปภาพ'
        advice = 'ข้อแนะนำ - เปลี่ยนชื่อไฟล์เป็นภาษาอังกฤษ'
        context = {'get_img' : get_img,
            'get_order' : get_order,
            'myStore' : myStore,
            'totel_product' : totel_product,
            'waitcheck_order' : waitcheck_order,
            'waitpay_order' : waitpay_order,
            'refund_order' : refund_order,
            'count_all' : count_all,
            'error_txt' : error_txt,
            'advice' : advice,
        }
        return render(request, template_name='covert_image.html', context=context)

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
            return redirect('product_desc', id=product.id)
        if amount != 1:
            error_amount = 'กรุณาสั่งซื้อใหม่ เนื่องจากไม่มีการแกะลายสามารถสั่งได้ทีละลูก'
            context = {'error_amount' : error_amount}
            return redirect('product_desc', id=product.id)

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

    if order.State_id.id == 1:
        state = State.objects.get(id=7)
        order.State_id = state

    else:
        state = State.objects.get(id=6)
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

        if order.State_id.id == 1:
            state = State.objects.get(id=7)
        else:
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
    
@login_required
def farm_refund(request, id):
    order = Order.objects.get(id=id)
    state = State.objects.get(id=7)
    order.State_id = state
    order.save()
    return redirect('historyorder')

@login_required
def send_review(request, id):
    order = Order.objects.get(id=id)
    product = order.product_id.product_image
    state = State.objects.get(id=8)
    order.State_id = state
    order.save()
    review_description = request.POST.get('review_description')
    review_rating = request.POST.get('review_rating')
    review_image = request.FILES.get('review_image')
    if review_image == None:
        my_review = Review.objects.create(review_description=review_description, review_rating=review_rating, review_image=product, order_id=order)
    else:
        my_review = Review.objects.create(review_description=review_description, review_rating=review_rating, review_image=review_image, order_id=order)
    my_review.save()
    return redirect('orderstatus')