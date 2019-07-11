from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserLoginForm

def login(request):
    if request.method != 'POST':
         return JsonResponse({"err_code": "4.3", "err_msg": "Please use 'POST' method."})
    else:
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return JsonResponse({"err_code":"100", "err_msg":"Login successfully!"})
            else:
                return JsonResponse({"err_code":"101", "err_msg":"Wrong password or username!"})
        else:
            return JsonResponse({"err_code": "102", "err_msg": "invalid"})


def logout_view(request):
    """注销用户"""
    if request.method != 'POST':
         return JsonResponse({"err_code": "4.3", "err_msg": "Please use 'POST' method."})
    else:
        logout(request)
        return JsonResponse({"err_code": "200", "err_msg": "Logout successfully!"})

def register(request):
    """注册新用户"""
    if request.method != 'POST':
         return JsonResponse({"err_code": "4.3", "err_msg": "Please use 'POST' method."})
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return JsonResponse({"err_code": "300", "err_msg": "Login successfully!"})
        else:
            return JsonResponse({"err_code": "301", "err_msg": "invalid"})
