import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .utils import UserInfoClean, get_info_from_request, backend_login_required


def backend_login(request):
    """Login given request

    `username`, `password` in request.POST['login_info'] are required
    """
    login_attr = ('username', 'password')
    login_info = get_info_from_request(
        request, 'POST', 'login_info', login_attr)
    current_user = authenticate(**login_info)
    if current_user is not None:
        login(request, current_user)
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({
            'error_code': '401001',
            'message': 'username or password error'
        }, status=401)


def backend_logout(request):
    """Logout given request"""
    logout(request)
    return JsonResponse({}, status=200)


def backend_register(request):
    """Register a new user with default permission

    `username`, `password` in request.POST['register_info'] are required.
    `email`, `first_name`, `last_name` in request.POST['register_info'] are
    optional.
    """
    register_attr = (
        'username', 'email', 'password', 'first_name', 'last_name')
    register_info = get_info_from_request(
        request, 'POST', 'register_info', register_attr)
    if User.objects.filter(username=register_info['username']).count():
        return JsonResponse({
            'error_code': '409001',
            'message': 'duplicate username'
        }, status=409)
    try:
        clean_tool = UserInfoClean()
        clean_tool.register_clean(register_info)
    except ValidationError as error:
        error_info = error.message_dict
        return JsonResponse({
            'error_code': '400' + error_info['error_code'][0],
            'message': 'invailed user information:\
             %s' % error_info['message'][0]
        }, status=400)
    User.objects.create_user(**register_info)
    return JsonResponse({}, status=201)


@backend_login_required
def backend_profile_show(request):
    """Return the profile of current user

    Login required.

    `username`, `email`, `first_name`, `last_name` are returned in
    response.content['profile'] even when they are blank.
    """
    user_plain_attr = ('username', 'email', 'first_name', 'last_name')
    return JsonResponse({
        'profile': {
            attr: getattr(request.user, attr) for attr in user_plain_attr
        }
    }, status=200)


@backend_login_required
def backend_profile_edit(request):
    """Edit the profile of current user according the given information

    Login required.
    `email`, `first_name`, `last_name` are optional.
    """
    profile_attr = ('password', 'email', 'first_name', 'last_name')
    new_profile = get_info_from_request(
        request, 'POST', 'new_profile', profile_attr)
    if 'password' in new_profile.keys():
        request.user.set_password(new_profile['password'])
        new_profile.pop('password')
    try:
        clean_tool = UserInfoClean()
        clean_tool.profile_edit_clean(new_profile)
    except ValidationError as error:
        error_info = error.message_dict
        return JsonResponse({
            'error_code': '400' + error_info['error_code'][0],
            'message': 'invailed user information:\
             %s' % error_info['message'][0]
        }, status=400)
    for attr, value in new_profile.items():
        setattr(request.user, attr, value)
    request.user.save()
    return JsonResponse({}, status=200)
