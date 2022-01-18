from django.shortcuts import render, redirect
from .models import TypeUser, UserInType
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

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