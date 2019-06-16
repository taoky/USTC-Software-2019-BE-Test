import string
import re
import json
from django.core.exceptions import ValidationError
from django.http import JsonResponse


class UserInfoClean():
    """Limit user information formats

    `ValidationError` is raised with a dict containing `error_code` and
    `message` when some information is invailed or does not exist when required
    """
    def username_clean(self, username):
        if len(username) > 150:
            raise ValidationError({
                'error_code': '111',
                'message': 'too long username'
            })
        if len(username) == 0:
            raise ValidationError({
                'error_code': '112',
                'message': 'username can not be blank'
            })
        charset = string.ascii_letters + string.digits + '+-_.@'
        for letter in username:
            if letter not in charset:
                raise ValidationError({
                    'error_code': '113',
                    'message': 'username contains invailed character: \
                                "%s"' % letter
                })

    def first_name_clean(self, first_name):
        if len(first_name) > 30:
            raise ValidationError({
                'error_code': '121',
                'message': 'too long first_name'
            })

    def last_name_clean(self, last_name):
        if len(last_name) > 30:
            raise ValidationError({
                'error_code': '131',
                'message': 'too long last_name'
            })

    def email_clean(self, email):
        if len(email) > 100:
            raise ValidationError({
                'error_code': '141',
                'message': 'too long email'
            })
        pattern = r'[{0}]+@[{0}]+'.format('a-zA-Z0-9.-_')
        if not re.match(pattern, email):
            raise ValidationError({
                'error_code': '142',
                'message': 'email is invailed'
            })

    def password_clean(self, password):
        if len(password) > 128:
            raise ValidationError({
                'error_code': '151',
                'message': 'too long password'
            })
        if len(password) < 8:
            raise ValidationError({
                'error_code': '152',
                'message': 'too short password'
            })

    def profile_edit_clean(self, user_info):
        cleaned_attr = ('first_name', 'last_name', 'email', 'password')
        for attr in cleaned_attr:
            if attr in user_info.keys():
                getattr(self, attr + '_clean')(user_info[attr])

    def register_clean(self, user_info):
        force_cleaned_attr = ('username', 'password')
        for attr in force_cleaned_attr:
            try:
                getattr(self, attr + '_clean')(user_info[attr])
            except AttributeError:
                return ValidationError({
                    'error_code': '161',
                    'message': 'except attribute: %s' % attr
                })
        self.profile_edit_clean(user_info)


def get_info_from_request(request, method, info_name, attr_set):
    """Only get some attributes from request

    str `method`: HTTP method like 'POST' or 'GET'
    str `info_name`: Will get attributes from `request.POST[info_name]` if
    `method` is 'POST'
    tuple `attr_set`: All needed attributes

    Example: `get_info_from_request(request, 'POST', 'login_info', login_attr)`
    will get all attributes in `login_attr` from `request.POST['login_info']`.
    Then create a new dict and return it.
    """
    info_all = json.loads(getattr(request, method)[info_name])
    return {
        attr: info_all[attr]
        for attr in attr_set if attr in info_all.keys()
    }


def backend_login_required(view):
    """Make sure the user has logged in

    `401` is returned if the user has not logged in
    """
    def login_required_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error_code': '401000',
                'message': ''
            }, status=401)
        return view(request, *args, **kwargs)

    return login_required_view
