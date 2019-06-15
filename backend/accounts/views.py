import re

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from .username_validation import validate_username

User = get_user_model()


class LoginView(View):
    http_method_names = ['post', 'get']

    def get(self, requst):
        '''
        The normal login page
        '''
        pass

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            validate_username(username, False)
        except ValidationError as e:
            return JsonResponse({
                'code': 410,
                'msg': e.messages
            })

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return JsonResponse({
                'code': 200,
                'msg': ['Log in successfully']
            })
        else:
            return JsonResponse({
                'code': 400,
                'msg': ['Username or password is not correct']
            })


class RegisterView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        # The normal register page
        pass

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            validate_username(username, True)
        except ValidationError as e:
            return JsonResponse({
                'code': 410,
                'msg': e.messages
            })
        try:
            validate_password(password, request.user)
        except ValidationError as e:
            return JsonResponse({
                'code': 420,
                'msg': e.messages
            })
        User.objects.create_user(
            username=username, password=password
        )
        return JsonResponse({
            'code': 200,
            'msg': ['Register successfully']
        })


class ProfileView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        user = request.user

        return JsonResponse({
            'code': 200,
            'nickname': user.nickname,
            'phone_number': user.phone_number
        })

    def post(self, request):
        nickname = request.POST.get('nickname')
        phone_number = request.POST.get('phone_number')

        user = request.user

        user.nickname = nickname or user.nickname
        user.phone_number = phone_number or user.phone_number
        user.save(update_fields=['nickname', 'phone_number'])


class LogoutView(View):
    http_method_names = ['post']

    def post(self, request):
        if request.user.is_authenticated:
            auth_logout(request)
            return JsonResponse({
                'code': 200,
                'msg': ['Log out successfully']
            })
        else:
            return JsonResponse({
                'code': 401,
                'msg': ['Please log in first']
            })
