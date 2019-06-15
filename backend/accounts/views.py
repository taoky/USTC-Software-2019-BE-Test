import re

from django.contrib.auth import (
    get_user_model,
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

from .models import password_strength

User = get_user_model()

username_err_code = {
    1: '用户名未输入',
    2: '用户名已存在',
    3: '用户名不合法'
}


def is_username_valid(username, check_conflict):
    '''
    检查用户输入的用户名是否合法

    @param username: 用户提交的用户名
    @param check_conflict: 是否检查用户名已经存在
    @return: 若合法，返回0；
             否则，返回值约定如下：
             1 - 用户名未输入
             2 - 用户名已存在
             3 - 用户名中出现了除大小写字母、数字和下划线以外的字符
    '''
    if not username:
        return 1
    if User.objects.filter(username=username).exists():
        return 2
    if not re.search(u'^[_0-9a-zA-Z]+$', username):
        return 3
    return 0


password_err_code = {
    1: '长度不满足要求',
    2: '必须要有大写字母',
    3: '必须要有小写字母',
    4: '必须要有数字',
    5: '必须要有特殊字符',
    6: '密码未输入'
}


def is_password_valid(password, strength):
    '''
    检查密码强度是否符合要求

    @param password: 用户提交的密码
    @param strength: 系统定义的强度要求，为一个dict，包含
                        min_length: 最短要求的密码长度
                        upper: 是否要求有大写字母
                        lower: 是否要求有小写字母
                        num: 是否要求有数字
                        symbol: 是否要求有特殊字符
    @return: 若合法，返回0
             否则，返回值约定如下
             1 - 长度不满足要求
             2 - 不含有要求的大写字母
             3 - 不含有要求的小写字母
             4 - 不含有要求的数字
             5 - 不含有要求的特殊字符
             6 - 密码未输入
    '''
    if not password:
        return 6

    min_length = strength.get('min_length', 0)
    upper = strength.get('upper', False)
    lower = strength.get('lower', False)
    num = strength.get('num', False)
    symbol = strength.get('symbol', False)

    if len(password) < min_length:
        return 1
    if upper:
        match = re.findall('[A-Z]+', password)
        if not match:
            return 2
    if lower:
        match = re.findall('[a-z]+', password)
        if not match:
            return 3
    if num:
        match = re.findall('[0-9]+', password)
        if not match:
            return 4
    if symbol:
        match = re.search(u'^[_0-9a-zA-Z]+$', password)
        if match:
            return 5
    return 0


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

        username_err = is_username_valid(username, False)
        if username_err:
            return JsonResponse({
                'code': 410 + username_err,
                'msg': username_err_code[username_err]
            })
        # password_err = is_password_valid(password, password_strength)
        # if password_err:
        #     return JsonResponse({
        #         'code': 420 + password_err,
        #         'msg': password_err_code[password_err]
        #     })

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return JsonResponse({
                'code': 200,
                'msg': '登陆成功'
            })
        else:
            return JsonResponse({
                'code': 400,
                'msg': '用户名或密码不正确'
            })


class RegisterView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        # The normal register page
        pass

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        username_err = is_username_valid(username, True)
        if username_err:
            return JsonResponse({
                'code': 410 + username_err,
                'msg': username_err_code[username_err]
            })
        password_err = is_password_valid(password, password_strength)
        if password_err:
            return JsonResponse({
                'code': 420 + password_err,
                'msg': password_err_code[password_err]
            })
        User.objects.create_user(
            username=username, password=password
        )
        return JsonResponse({
            'code': 200,
            'msg': '注册成功'
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
                'msg': '退出成功'
            })
        else:
            return JsonResponse({
                'code': 401,
                'msg': '请先登录'
            })
