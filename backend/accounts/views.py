import re

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.password_validation import (password_changed,
                                                     validate_password)
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from accounts.mixin import LoginRequiredMixin
from accounts.username_validation import validate_username

User = get_user_model()


class LoginView(View):
    '''
    返回用户登录时的界面以及处理用户提交的登录请求
    不要求登录
    '''
    http_method_names = ['post', 'get']

    def get(self, requst):
        '''
        The normal login page
        '''
        pass

    def post(self, request):
        '''
        处理用户对于```/accounts/login```的post请求
        处理用户登录时的用户密码，并进行验证。若用户密码正确，则将用户登录至系统中

        @param in POST
            username<str>:  请求登录的用户名
            password<str>:  相应的密码

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义             |
                       | ------ | ---------------- |
                       | 200    | 注册成功         |
                       | 410    | 用户名不符合要求 |
                       | 420    | 密码不符合要求   |
            msg<dict>:  返回代码相应的解释
        '''
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # 检查用户名是否符合要求
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
    '''
    返回用户注册时的界面以及处理用户提交的注册请求
    不要求登录
    '''
    http_method_names = ['get', 'post']

    def get(self, request):
        # The normal register page
        pass

    def post(self, request):
        '''
        处理用户对于```/accounts/register```的post请求
        处理用户注册提交的注册信息，若用户名和密码符合要求，将用户添加至系统中

        @param in POST
            username<str>:  请求注册的用户名
            password<str>:  相应的密码

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义             |
                       | ------ | ---------------- |
                       | 200    | 注册成功         |
                       | 410    | 用户名不符合要求 |
                       | 420    | 密码不符合要求   |
            msg<dict>:  返回代码相应的解释
        '''
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # 检查用户名是否符合要求
            validate_username(username, True)
        except ValidationError as e:
            return JsonResponse({
                'code': 410,
                'msg': e.messages
            })
        try:
            # 检查密码是否符合要求
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


class ChangePasswordView(LoginRequiredMixin, View):
    '''
    处理用户修改密码的请求
    **要求登录**
    '''
    http_method_names = ['post']

    def post(self, request):
        '''
        处理用户对于```/accounts/change_password```的post请求
        处理用户的修改密码的请求

        @param in POST
            old_password<str>:  旧密码
            new_password<str>:  新密码

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义               |
                       | ------ | ------------------ |
                       | 200    | 修改密码成功       |
                       | 400    | 旧的密码错误       |
                       | 401    | 未登录             |
                       | 420    | 新的密码不符合要求 |
            msg<dict>:  返回代码相应的解释
        '''
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        try:
            password_changed(new_password, request.user)
        except ValidationError as e:
            return JsonResponse({
                'code': 420,
                'msg': e.messages
            })
        user = authenticate(
            request, username=request.user.username, password=old_password)
        if user:
            user.set_password(new_password)
            user.save()
            return JsonResponse({
                'code': 200,
                'msg': ['Change password successfully']
            })
        else:
            return JsonResponse({
                'code': 400,
                'msg': ['The old password is not correct']
            })


class ProfileView(LoginRequiredMixin, View):
    '''
    返回用户的个人信息以及处理用户更新个人信息的请求
    **要求登录**
    '''
    http_method_names = ['get', 'post']

    def get(self, request):
        '''
        处理用户对于```/accounts/profile```的get请求
        返回用户个个人信息

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义                   |
                       | ------ | ---------------------- |
                       | 200    | 正常返回用户的个人信息 |
                       | 401    | 未登录                 |
            msg<str>:  
        '''
        user = request.user

        return JsonResponse({
            'code': 200,
            'nickname': user.nickname,
            'phone_number': user.phone_number
        })

    def post(self, request):
        '''
        处理用户对于```/accounts/profile```的post请求
        处理用户修改个人信息的请求

        @param in POST
            nickname<str>:  用户的昵称
            new_password<str>:  新密码

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义                   |
                       | ------ | ---------------------- |
                       | 200    | 正常返回用户的个人信息 |
                       | 401    | 未登录                 |
            msg<str>:  返回代码相应的解释
        '''
        nickname = request.POST.get('nickname')
        phone_number = request.POST.get('phone_number')

        if phone_number and not re.search('^[0-9-+]*$', phone_number):
            return JsonResponse({
                'code': 400,
                'msg': ['Invalid phone number']
            })

        user = request.user

        user.nickname = nickname or user.nickname
        user.phone_number = phone_number or user.phone_number
        user.save(update_fields=['nickname', 'phone_number'])

        return JsonResponse({
            'code': 200,
            'msg': ['Update profile successfully']
        })


class LogoutView(LoginRequiredMixin, View):
    '''
    处理用户的退出请求
    **需要登录**
    '''
    http_method_names = ['post']

    def post(self, request):
        '''
        处理用户对于```/accounts/logout```的post请求
        将用户从系统中登出

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义     |
                       | ------ | -------- |
                       | 200    | 登录成功 |
                       | 401    | 未登录   |
            msg<str>:  返回代码相应的解释
        '''
        auth_logout(request)
        return JsonResponse({
            'code': 200,
            'msg': ['Log out successfully']
        })
