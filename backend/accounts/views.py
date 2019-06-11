import json
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class JsonHttpResponse(HttpResponse):
    def __init__(self, status_code, data={}, *args, **kwargs):
        """Returned object. To return json as response to the client.

        `status_code`: Int following RESTful rules
        `data`: Should be a dict to be converted to json as response
        """
        content = json.dumps(data)
        kwargs['status'] = status_code
        kwargs['content_type'] = 'application/json'
        kwargs['charset'] = 'utf-8'
        super(JsonHttpResponse, self).__init__(content, *args, **kwargs)


def backend_login(request):
    """Use `username` and `password` in request.POST['login_info'] to login"""
    login_info = {
        'username': request.POST['login_info']['username'],
        'password': request.POST['login_info']['password']
    }
    current_user = authenticate(**login_info)
    if current_user is not None:
        login(request, current_user)
        return JsonHttpResponse(200)
    else:
        error_info = {
            'error_code': 401001,
            'message': 'username or password error'
        }
        return JsonHttpResponse(401, error_info)


def backend_logout(request):
    logout(request)
    return JsonHttpResponse(200)


def backend_register(request):
    """Use `username`, `password` and `email` in request.POST['register_info']
    to register"""
    register_info = {
        'username': request.POST['register_info']['username'],
        'email': request.POST['register_info']['email'],
        'password': request.POST['register_info']['password']
    }
    if User.objects.filter(username=register_info['username']).count():
        error_info = {
            'error_code': 409001,
            'message': 'duplicate username'
        }
        return JsonHttpResponse(409, error_info)
    User.objects.create_user(**register_info)
    return JsonHttpResponse(201)


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
        return JsonHttpResponse(401)
    if request.POST['profile']['method'] == 'show':
        user_plain_attr = ('username', 'email', 'first_name', 'last_name')
        user_info = {
            attr: getattr(request.user, attr) for attr in user_plain_attr
        }
        user_info['password'] = 'currently not return this'
        return JsonHttpResponse(200, user_info)
    elif request.POST['profile']['method'] == 'edit':
        if 'password' in request.POST['profile']['new_profile'].keys():
            new_password = ['profile']['new_profile']['password']
            if request.user.check_password(new_password):
                request.user.set_password(new_password)
            else:
                error_info = {
                    'error_code': 400001,
                    'message': 'invailed password'
                }
                return JsonHttpResponse(400, error_info)
        user_plain_editable_attr = ('email', 'first_name', 'last_name')
        for attr in user_plain_editable_attr:
            if attr in request.POST['profile']['new_profile'].keys():
                setattr(request.user, attr,
                        request.POST['profile']['new_profile'][attr])
        return JsonHttpResponse(200)
    else:
        return JsonHttpResponse(204)
