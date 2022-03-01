from django.shortcuts import render, redirect, get_object_or_404
from user.models import TypeUser, UserInType
from .models import State, Order, Review
from store.models import Store, TypeeOrder, Quality, Product
from .models import Message
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf 
from django.template.loader import render_to_string
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
    return render(request, template_name='chatroom.html')

@login_required
def order_list(request, id):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore.id)
    totel_product = len(totel_product)

    type_state = State.objects.all()
    product_order = Product.objects.get(id=id)

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'product_order' : product_order,
        'type_state' :type_state,}

    return render(request, template_name='order_list.html', context=context)

@login_required
def payment_order(request):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore.id)
    totel_product = len(totel_product)


    context = {'myStore' : myStore,
        'totel_product' : totel_product,

       }
    return render(request, template_name='payment_order.html', context=context)

@login_required
def report_order(request):
    user = request.user
    myStore = Store.objects.get(user_id=user)
    totel_product = Product.objects.filter(store_id=myStore.id)
    totel_product = len(totel_product)
    quality_list = Quality.objects.all()


    # img = cv2.imread(myStore.store_logo.url, 0)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.imshow('image', img)

    # cv2.imwrite('data/dst/lena_opencv_red.jpg', im)





    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'quality_list' :quality_list,
        
       }
    return render(request, template_name='report_order.html', context=context)
