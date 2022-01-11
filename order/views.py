from django.shortcuts import render, redirect, get_object_or_404
from order.models import State, Order, Review
from django.contrib.auth.models import User, Group

from store.models import Store
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

