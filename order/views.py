from django.shortcuts import render, redirect, get_object_or_404
from user.models import TypeUser, UserInType
from .models import State, Order, Review
from store.models import Store, TypeeOrder, Quality, Product
from .models import Message
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf 
from django.template.loader import render_to_string

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # pk = kwargs.get('pk')
        # order = get_object_or_404(Order, pk=pk)
        user = request.user
        store = Store.objects.get(user_id=user)
        open('templates/temp.html', "w").write(render_to_string('waybill.html', {'store': store}))
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

    context = {'myStore' : myStore,
        'totel_product' : totel_product,
        'quality_list' :quality_list,

       }
    return render(request, template_name='report_order.html', context=context)
