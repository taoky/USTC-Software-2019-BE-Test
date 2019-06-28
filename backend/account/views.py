from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import RegistrationForm, LoginForm

def regist(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password_re']
            #Using User method to create a new account
            user = User.objects.create_user(username=username, password=password)
            return HttpResponse("Registration successful!")
        else:
            errors = form.errors
            return JsonResponse({"err_msg":errors})
    else:
        return HttpResponse("Please use 'POST' method!")

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            #Using auth mod to check
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponse("Login successfully.")
            else:
                return HttpResponse("Wrong password!")
        else:
            errors = form.errors
            return JsonResponse({"err_msg":errors})





