import json
import hashlib
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class JsonHttpResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        content = json.dumps(data)
        kwargs['content_type'] = 'application/json'
        super(JsonHttpResponse, self).__init__(content, *args, **kwargs)


def backend_login(request):
    """Use `username` and `password` in request.POST to login"""
    login_info = {
        'username': request.POST['username'],
        'password': request.POST['password']
    }
    current_user = authenticate(**login_info)
    if current_user is not None:
        login(request, current_user)
        response = {
            'status_code': 200,
            'message': 'success'
        }
    else:
        response = {
            'status_code': 400,
            'message': 'username or password error'
        }
    return JsonHttpResponse(response)


def backend_logout(request):
    if request.user.is_authenticated:
        logout(request)
        response = {
            'status_code': 200,
            'message': 'success'
        }
    else:
        response = {
            'status_code': 400,
            'message': 'not logged in yet'
        }
    return JsonHttpResponse(response)


def backend_register(request):
    """Use `username`, `password` and `email` in request.POST to register"""
    register_info = {
        'username': request.POST['username'],
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    if request.user.is_authenticated:
        response = {
            'status_code': 400,
            'message': 'have logged in'
        }
    elif User.objects.filter(username=register_info['username']).count():
        response = {
            'status_code': 400,
            'message': 'duplicate username'
        }
    else:
        User.objects.create_user(**register_info)
        response = {
            'status_code': 200,
            'message': 'success'
        }
    return JsonHttpResponse(response)


def backend_profile_show(request):
    """Show information of current user. Results are in response.content"""
    if not request.user.is_authenticated:
        response = {
            'status_code': 400,
            'message': 'not logged in yet'
        }
    else:
        user_plain_attr = ('username', 'email', 'first_name', 'last_name')
        user_info = {
            attr: getattr(request.user, attr) for attr in user_plain_attr
        }
        user_info['password'] = 'currently not return this'
        response = {
            'status_code': 200,
            'message': 'success',
            'content': user_info
        }
    return JsonHttpResponse(response)


def backend_profile_edit(request):
    """Use attribute names and values in request.POST to edit user profile"""
    if not request.user.is_authenticated:
        response = {
            'status_code': 400,
            'message': 'not logged in yet'
        }
    else:
        if 'password' in request.POST:
            if request.user.check_password(request.POST['password']):
                request.user.set_password(request.POST['password'])
            else:
                response = {
                    'status_code': 400,
                    'message': 'invailed password'
                }
                return JsonHttpResponse(response)
        user_plain_editable_attr = ('email', 'first_name', 'last_name')
        for attr in user_plain_editable_attr:
            if attr in request.POST:
                setattr(request.user, attr, request.POST[attr])
        response = {
            'status_code': 200,
            'message': 'success'
        }
    return JsonHttpResponse(response)
