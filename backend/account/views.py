from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .models import UserForm, LoginForm, User


def index(request):
    return HttpResponse("You are in the index")

def login(request):
    if request.method == 'POST':
        userform = LoginForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return redirect('/index/')
                else:
                    message = 'incorrect password'
            except:
                massage="The user doesn't exist"
        return redirect('/login/')
    else:
        return HttpResponse('You are in the login')
        

def register(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            user = User()
            user.name = userform.cleaned_data['username']
            user.password = userform.cleaed_data['password']
            user.gender = userform['gender']
            user.email = userform['email']
            massage = 'registered successfully'
    else:
        return HttpResponse('You are in the register')

def logout(request):
    return HttpResponse('You are in the logout')
# Create your views here.
