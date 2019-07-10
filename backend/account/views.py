from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from . import models
from .models import RegisterForm, LoginForm, UpdateForm,User
import json
from django.core import serializers

def index(request):
    resp={"err_code":"000","message":"You are in the index"}
    return JsonResponse(resp)

def login(request):
    """"""
    if request.method == 'POST':
        user_form = LoginForm(request.POST)#
        cd_data = userform.cleaned_data#request.POST.dict()
        if user_form.is_valid():#True:
            username = cd_data['username']
            password = cd_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['username'] = username
                    resp={"err_code":"101","message":"Login successfully"}
                    return JsonResponse(resp)
                else:
                    resp={"err_code":"102","message":"Wrong password"}
                    return JsonResponse(resp)
            except:
                resp={"err_code":"103","message":"User does not exist"}
                return JsonResponse(resp)
        else:
            resp={"err_code":"104","message":"Input invalid"}
    else:
        resp={"err_code":"100","message":"You are in the login"}
        return JsonResponse(resp)
        

def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)#
        cd_data = user_form.cleaned_data#request.POST.dict()
        if user_form.is_valid():#True:
            if cd_data['password'] == cd_data['repassword']:
                user = User()
                user.name = cd_data['username']
                user.password = cd_data['password']
                user.sex = cd_data['sex']
                user.email = cd_data['email']
                user.save()
                request.session['username'] = user.name
                resp={"err_code":"201","message":"Registered seccessfully"}
                return JsonResponse(resp) 
            else:
                resp={"err_code":"203","message":"please input password again"}
                return JsonResponse(resp)
        else:
            resp={"err_code":"202","message":"Input invalid"}
            return JsonResponse(resp)
    else:
        resp={"err_code":"200","message":"You are in the register"}
        return JsonResponse(resp)

def logout(request):
    try:
        del request.session['username']
    except KeyError:
        resp={"err_code":"301","message":"session cancelled already"}
        return JsonResponse(resp)
    resp={"err_code":"300","message":"Logout successfully"}
    return JsonResponse(resp)

def user_index(request):
    """the information of the user which is identified through session"""
    try:
        username = request.session['username']
    except KeyError:
        resp={"err_code":"401","message":"Permission denied"}
        return JsonResponse(resp)
    user = models.User.objects.get(name=username)
    resp = {"err_code":"400",'username':user.name,'password':user.password,'sex':user.sex,'email':user.email}
    return JsonResponse(resp)

def update_user_index(request):

    if request.method == "POST":
        try:
            username = request.session['username']
        except KeyError:
            resp={"err_code":"501","message":"Permission denied"}
            return JsonResponse(resp)
        u_user = models.User.objects.get(name=username)

        update_form = UpdateForm(request.POST)#
        cd_data = update_form.cleaned_data#request.POST.dict()
        if update_form.is_valid:#True
            if cd_data['re_new_password'] == cd_data['new_password']:
                u_user.password = cd_data['new_password']
                u_user.sex = cd_data['new_sex']
                u_user.email = cd_data['new_email']
                u_user.is_active=True
                u_user.save()
                resp={"err_code":"502","message":"Updated successfully"}
                return JsonResponse(resp)
            else:
                resp={"err_code":"503","message":"Please input password again"}
                return JsonResponse(resp)
        else:
            resp={"err_code":"504","message":"Invalid input"}
            return JsonResponse(resp)
    else:
        try:
            username = request.session['username']
        except KeyError:
            resp={"err_code":"501","message":"Permission denied"}
            return JsonResponse(resp)
        resp={"err_code":"500","message":"You are in the update_user_index"}
        return JsonResponse(resp)


    

# Create your views ere.
