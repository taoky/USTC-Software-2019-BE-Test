from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.
def login_view(request):
    """
    login to your account
    (I use django built-in authentication system,
    and I refer to last year's requirements)
    :param request:
    :return: JsonResponse
    | err_code |               err_msg                |               description                |
    | :------: | :----------------------------------: | :--------------------------------------: |
    |    0     |                  ''                  |                 Success                  |
    |    1     |   'No such user or wrong password'   |     Wrong username or wrong password     |
    |    2     |     'Please logout before login'     | You haven't logged out before logging in |
    |    3     | 'Please enter username and password' |     Not type in username or password     |
    """
    ret_json = {
        'err_code': 0,
        'err_msg': '',
    }

    # you are not allowed to login before logout
    if request.user.is_authenticated:
        ret_json['err_code'] = 2
        ret_json['err_msg'] = 'Please logout before login'
    else:
        if request.method == 'POST':
            try:
                username = request.POST['username']
                password = request.POST['password']
            except KeyError:
                ret_json['err_code'] = 3
                ret_json['err_msg'] = 'Please enter username and password'
                return JsonResponse(ret_json)

            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                # leave the work to django session framework
                login(request=request, user=user)
                # redundancy. Just to make it explicit
                ret_json['err_code'] = 0
                ret_json['err_msg'] = ''

            else:
                ret_json['err_code'] = 1
                ret_json['err_msg'] = 'No such user or wrong password'

    return JsonResponse(ret_json)


def logout_view(request):
    """
    log out
    :param request:
    :return: JsonResponse
    | err_code |        err_msg        |       description       |
    | :------: | :-------------------: | :---------------------: |
    |    0     |          ''           |         Success         |
    |    1     | 'Logout before login' | You should log in first |
    """
    ret_json = {
        'err_code': 0,
        'err_msg': ''
    }

    if request.user.is_authenticated:
        logout(request)
    else:
        # It's ok to do that, but I will throw some warnings on that.
        ret_json['err_code'] = 1
        ret_json['err_msg'] = 'Logout before login'

    return JsonResponse(ret_json)


def register_view(request):
    """
    register an account
    :param request:
    :return:
    | err_code |               err_msg                |           description            |
    | :------: | :----------------------------------: | :------------------------------: |
    |    0     |                  ''                  |             Success              |
    |    1     | 'Please enter username and password' | Not type in username or password |
    |    2     |    'This username has been used'     |   This username has been used    |
    """
    ret_json = {
        'err_code': 0,
        'err_msg': '',
    }

    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            ret_json['err_code'] = 1
            ret_json['err_msg'] = "Please enter username and password"
            return JsonResponse(ret_json)
        else:
            if not username or not password:
                ret_json['err_code'] = 1
                ret_json['err_msg'] = "Please enter username and password"
                return JsonResponse(ret_json)

            if User.objects.filter(username=username).exists():
                ret_json['err_code'] = 2
                ret_json['err_msg'] = 'This username has been used'
                return JsonResponse(ret_json)
            else:
                User.objects.create_user(username=username, password=password)
                return JsonResponse(ret_json)

    else:
        return JsonResponse(ret_json)


