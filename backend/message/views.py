import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from message.models import Message
from backend.utils import backend_login_required, get_info_from_request
from message.utils import MessageInfoClean


@backend_login_required
def message_send(request):
    message_attr = ('hidden_seconds', 'content')
    message_info = get_info_from_request(
        request, 'POST', 'message_info', message_attr)
    # Message info clean
    clean_tool = MessageInfoClean()
    try:
        clean_tool.message_send_clean(message_info)
    except ValidationError as error:
        error_info = error.message_dict
        return JsonResponse({
            'error_code': '400' + error_info['error_code'][0],
            'message': 'invailed message information:\
             %s' % error_info['message'][0]
        }, status=400)
    new_message = Message(**message_info, owner=request.user)
    new_message.save()
    return JsonResponse({}, status=201)


@backend_login_required
def message_recieve(request):
    messages = Message.objects.filter(
        owner=request.user).order_by('-sent_time')
    return JsonResponse({
        'messages': [
            {
                'sent_time': message.sent_time.isoformat(),
                'recieved_time': message.recieved_time.isoformat(),
                'hidden_seconds': message.hidden_seconds,
                **({
                    'content': message.content
                } if message.recieved_time < timezone.now() else {})
            }
            for message in messages
        ]
    }, status=200)
