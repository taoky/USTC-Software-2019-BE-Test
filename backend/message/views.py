import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone

from message.models import Message
from backend.utils import backend_login_required, get_info_from_request


@backend_login_required
def message_send(request):
    message_attr = ('hidden_time', 'content', 'reciever')
    message_info = get_info_from_request(
        request, 'POST', 'message_info', message_attr)
    # Message info clean
    if len(message_info['content']) > 255:
        return JsonResponse({
            'error_code': 400211,
            'message': 'too long content'
        })
    new_message = Message(**message_info)
    new_message.save()
    return JsonResponse({}, status=201)


@backend_login_required
def message_recieve(request):
    messages = Message.objects.filter(
        owner=request.user).order_by('-recieved_time')
    return JsonResponse({
        'messages': [
            {
                'sent_time': message.sent_time.isoformat(),
                'recieved_time': message.recieved_time.isoformat(),
                'hidden_seconds': message.hidden_seconds
            }.update({
                'content': message.content
            } if message.recieved_time < timezone.now else {})
            for message in messages
        ]
    }, status=200)
