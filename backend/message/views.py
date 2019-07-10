from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import dateparse

from datetime import datetime

from .models import Message


# Create your views here.
def index_view(request, username):
    """
    view user's messages
    due to the same reason with UserProfile,
    I pass username as a parameter
    :param request:
    :param username: username of messages
    :return:
    | err_code |       err_msg       |                         description                          | Other Properties |
    | :------: | :-----------------: | :----------------------------------------------------------: | :--------------: |
    |    0     |         ''          |                           Success                            |     messages     |
    |    1     |   'No such user'    |                         No such user                         |        -         |
    |    2     | 'Permission denied' | You haven't logged in or you have no access to messages.     |        -         |
    """
    ret_json = {
        'err_code': 0,
        'err_msg': '',
    }

    if not request.user.is_authenticated or request.user.username != username:
        ret_json['err_code'] = 2
        ret_json['err_msg'] = 'Permission denied'
        return JsonResponse(ret_json)

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        ret_json['err_code'] = 1
        ret_json['err_msg'] = 'No such user'
        return JsonResponse(ret_json)
    else:
        messages = list(user.message_set.filter(available_time__lt=datetime.now()))
        ret_json['messages'] = messages
        return JsonResponse(ret_json)


def create_view(request, username):
    """
    create a new message
    :param request: a legal request.POST dict may contain:
    |   property    |                         description                          |
    | :-----------: | :----------------------------------------------------------: |
    | 'msg_content' |                    content of the message                    |
    |  'duration'   | Certain amount of time this message will be hided.           |
                      Format: "**DD** **HH:MM:SS.uuuuuu**". Default zero if not set|
                      (e.g. "1":  one second,
                            "01:01:01": 3661 seconds,
                            "21 01:01:01": 21 days and 3661 seconds)
    :param username: username of the message
    :return:
    | err_code |       err_msg       |                         description                          | Other Properties |
    | :------: | :-----------------: | :----------------------------------------------------------: | :--------------: |
    |    0     |         ''          |                           Success                            |        -         |
    |    1     |   'No such user'    |                         No such user                         |        -         |
    |    2     | 'Permission denied' | You haven't logged in or you have no access to messages.     |        -         |
    |    3     | 'Parameter missing' | You have to pass in duration.                                |        -         |
    """
    ret_json = {
        'err_code': 0,
        'err_msg': '',
    }

    if not request.user.is_authenticated or request.user.username != username:
        ret_json['err_code'] = 2
        ret_json['err_msg'] = 'Permission denied'
        return JsonResponse(ret_json)

    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            ret_json['err_code'] = 1
            ret_json['err_msg'] = 'No such user'
            return JsonResponse(ret_json)
        else:
            duration = request.POST.get('duration') or '0'
            content = request.POST.get('msg_content') # it's ok to be none
            duration = dateparse.parse_duration(duration)
            created_time = datetime.now()
            available_time = created_time + duration

            Message.objects.create(user=user,
                                   content=content,
                                   created_time=created_time,
                                   available_time=available_time)

    else:
        return JsonResponse(ret_json)




