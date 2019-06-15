import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def backend_login(request):
    """Login given request

    `username`, `password` in request.POST['login_info'] are required
    """
    login_info_all = json.loads(request.POST['login_info'])
    login_info = {
        'username': login_info_all['username'],
        'password': login_info_all['password']
    }
    current_user = authenticate(**login_info)
    if current_user is not None:
        login(request, current_user)
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({
            'error_code': 401001, 'message': 'username or password error'
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
    register_info_all = json.loads(request.POST['register_info'])
    register_available_attr = (
        'username', 'email', 'password', 'first_name', 'last_name'
    )
    register_info = {
        attr: register_info_all[attr]
        for attr in register_available_attr if attr in register_info_all.keys()
    }
    if User.objects.filter(username=register_info['username']).count():
        return JsonResponse({
            'error_code': 409001, 'message': 'duplicate username'
        }, status=409)
    try:
        validate_password(register_info['password'])
    except ValidationError as error:
        return JsonResponse({
            'error_code': 400001, 'message': 'invailed password: %s' % error
        }, status=400)
    User.objects.create_user(**register_info)
    return JsonResponse({}, status=201)


def backend_profile_show(request):
    """Return the profile of current user

    Login required.

    `username`, `email`, `first_name`, `last_name` are returned in
    response.content['profile'] even when they are blank.
    """
    if not request.user.is_authenticated:
        return JsonResponse({}, status=401)
    user_plain_attr = ('username', 'email', 'first_name', 'last_name')
    return JsonResponse({
        'profile': json.dumps({
            attr: getattr(request.user, attr) for attr in user_plain_attr
        })
    }, status=200)


def backend_profile_edit(request):
    """Edit the profile of current user according the given information

    Login required.
    `email`, `first_name`, `last_name` are optional.
    """
    new_profile = json.loads(request.POST['new_profile'])
    if 'password' in new_profile.keys():
        new_password = new_profile['password']
        try:
            validate_password(new_password, user=request.user)
        except ValidationError as error:
            return JsonResponse({
                'error_code': 400001, 'message': 'invailed password: %s' % error
            }, status=400)
        request.user.set_password(new_password)
    user_plain_editable_attr = ('email', 'first_name', 'last_name')
    for attr in user_plain_editable_attr:
        if attr in new_profile.keys():
            setattr(request.user, attr, new_profile[attr])
    request.user.save()
    return JsonResponse({}, status=200)
