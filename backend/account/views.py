from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("You are in the index")

def login(request):
    return HttpResponse('You are in the login')

def register(request):
    return HttpResponse('You are in the register')

def logout(request):
    return HttpResponse('You are in the logout')
# Create your views here.
