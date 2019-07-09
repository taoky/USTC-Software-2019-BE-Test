from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .models import RegisterForm, LoginForm, UpdateForm
import json
from django.core import serializers

def index(request):
    resp={"err_code":"000","message":"You are in the index"}
    return HttpResponse(json.dumps(resp),content_type="application/json")

def login(request):
    if request.method == 'POST':
        userform = LoginForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['username'] = username
                    resp={"err_code":"101","message":"Login successfully"}
                    return HttpResponse(json.dumps(resp),content_type="application/json")
                else:
                    resp={"err_code":"102","message":"Wrong password"}
                    return HttpResponse(json.dumps(resp),content_type="application/json")
            except:
                resp={"err_code":"103","message":"User does not exist"}
                return HttpResponse(json.dumps(resp),content_type="application/json")
        else:
            resp={"err_code":"104","message":"Input invalid"}
    else:
       # empty_form = LoginForm()
       # data = serializers.serialize("json",emptyform.objects.all())
        resp={"err_code":"100","message":"You are in the login"}
        return HttpResponse(json.dumps(resp),content_type="application/json")
        

def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = User()
            user.name = user_form.cleaned_data['username']
            user.password = user_form.cleaed_data['password']
            user.gender = user_form['gender']
            user.email = user_form['email']
            user.save()
            request.session['username'] = user.name
            resp={"err_code":"201","message":"Registered seccessfully"}
            return HttpResponse(json.dumps(resp),content_type="application/json")
        else:
            resp={"err_code":"202","message":"Input invalid"}
            return HttpResponse(json.dumps(resp),content_type="application/json")
    else:
        resp={"err_code":"200","message":"You are in the register"}
        return HttpResponse(json.dumps(resp),content_type="application/json")

def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    resp={"err_code":"300","message":"Logout successfully"}
    return HttpResponse(json.dumps(resp),content_type="application/json")

def user_index(request):
    try:
        username = request.session['username']
    except KeyError:
        resp={"err_code":"401","message":"Permission denied"}
        return HttpResponse(json.dumps(resp),content_type="application/json")
    user = models.User.objects.get(name=username)
    resp = {"err_code":"400",'username':user.name,'password':user.password,'sex':user.gender,'email':user.email}
    return HttpResponse(json.dumps(resp),content_type="application/json")

def update_user_index(request):
    try:
        username = request.session['username']
    except KeyError:
        resp={"err_code":"500","message":"Permission denied"}
        return HttpResponse(json.dumps(resp),content_type="application/json")
    update_user = models.User.objects.get(name=username)
    if request.method == "POST":
        update_form = UpdateForm(request.POST)
        if update_form.is_valid:
            if update_form['old_password'] == update_form['new_password']:
                update_user.sex = update_form['new_gender']
                update_user.email = update_form['new_email']
                update_user.is_active=True
                update_user.save()
                resp={"err_code":"502","message":"Updated successfully"}
                return HttpResponse(json.dumps(resp),content_type="application/json")
            else:
                resp={"err_code":"503","message":"Please input password again"}
                return HttpResponse(json.dumps(resp),content_type="application/json")
        else:
            resp={"err_code":"504","message":"Invalid input"}
            return HttpResponse(json.dumps(resp),content_type="application/json")
    else:
       # empty_form = UpdateForm()
       # data = serializers.serialize("json",emptyform.objects.all())
        resp={"data":data,"err_code":"501","message":"You are in the update_user_index"}
        return HttpResponse(json.dumps(resp),content_type="application/json")


    

# Create your views ere.
