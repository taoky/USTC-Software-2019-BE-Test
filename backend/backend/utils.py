import json
from django.http import JsonResponse


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
