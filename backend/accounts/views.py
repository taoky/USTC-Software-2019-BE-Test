import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def backend_login(request):
    """Use `username` and `password` in request.POST['login_info'] to login"""
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
        error_info = {
            'error_code': 401001,
            'message': 'username or password error'
        }
        return JsonResponse(error_info, status=401)


def backend_logout(request):
    logout(request)
    return JsonResponse({}, status=200)


def backend_register(request):
    """Use `username`, `password` and `email` in request.POST['register_info']
    to register"""
    register_info_all = json.loads(request.POST['register_info'])
    register_info = {
        attr: register_info_all[attr]
        for attr in ('username', 'email', 'password', 'first_name', 'last_name')
        if attr in register_info_all.keys()
    }
    if User.objects.filter(username=register_info['username']).count():
        error_info = {
            'error_code': 409001,
            'message': 'duplicate username'
        }
        return JsonResponse(error_info, status=409)
    try:
        validate_password(register_info['password'])
    except ValidationError as error:
        error_info = {
            'error_code': 400001,
            'message': 'invailed password: %s' % error
        }
        return JsonResponse(error_info, status=400)
    User.objects.create_user(**register_info)
    return JsonResponse({}, status=201)


def backend_profile(request):
    """Show or edit the information of current user. The method is gained from
    request.POST['profile']['method'].

    If the method is `show`, return the information with putting it into
    response.profile
    If the method is `edit`, Use the new information in
    request.POST['profile']['new_profile'] to edit. If the information is not
    complete, the rest will be kept back.
    """
    if not request.user.is_authenticated:
        return JsonResponse({}, status=401)
    request_profile = json.loads(request.POST['profile'])
    if request_profile['method'] == 'show':
        user_plain_attr = ('username', 'email', 'first_name', 'last_name')
        user_info = {
            attr: getattr(request.user, attr) for attr in user_plain_attr
        }
        return JsonResponse(user_info, status=200)
    elif request_profile['method'] == 'edit':
        if 'password' in request_profile['new_profile'].keys():
            new_password = request_profile['new_profile']['password']
            try:
                validate_password(new_password, user=request.user)
            except ValidationError as error:
                error_info = {
                    'error_code': 400001,
                    'message': 'invailed password: %s' % error
                }
                return JsonResponse(error_info, status=400)
            request.user.set_password(new_password)
        user_plain_editable_attr = ('email', 'first_name', 'last_name')
        for attr in user_plain_editable_attr:
            if attr in request_profile['new_profile'].keys():
                setattr(request.user, attr,
                        request_profile['new_profile'][attr])
        request.user.save()
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=204)
