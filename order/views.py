from django.shortcuts import render
from order.models import State, Order, Review
from .models import Message
# Create your views here.
@login_required
def chatroom(request, id):
    return render(request, template_name='chatroom.html')