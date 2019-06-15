import json
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Message


# TODO: Classify error code with url
def message_send(request):
    if request.user.is_authenticate:
        return JsonResponse({}, status=401)
    message_info_all = json.loads(request.POST['message_info'])
    message_available_attr = ('hidden_time', 'content', 'reciever')
    message_info = {
        attr: message_info_all[attr] for attr in message_available_attr
    }
    try:
        reciever = User.objects.get(username=message_info['reciever'])
    except User.DoesNotexist:
        return JsonResponse({
            'error_code': 400002,
            'message': 'reciever does not exist'
        }, status=400)
    if len(message_info['content']) > 255:
        return JsonResponse({
            'error_code': 400003,
            'message': 'content is too long'
        })
    new_message = Message(**message_info,
                          sender=request.user, reciever=reciever)
    new_message.save()
    return JsonResponse({}, status=201)


def message_recieve(request):
    if request.user.is_authenticate:
        return JsonResponse({}, status=401)
