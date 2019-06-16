import datetime
import re
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic.base import View

from accounts.Mixin import LoginRequiredMixin
from msg.models import Message

from .models import model_to_dict


class CreateMessageView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        delay_time = request.POST.get('delay_time', '0:0:0:0')
        content = request.POST.get('content', '')
        public = request.POST.get('public', False)

        days, hours, minutes, seconds = list(
            map(int,
                map(lambda x: x or 0,
                    re.findall(
                        '([0-9]+):([0-9]+):([0-9]+):([0-9]+)', delay_time)[0]
                    )
                )
        )

        delta_time = datetime.timedelta(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )
        now = timezone.now()

        msg = Message(user=request.user, content=content, uuid=uuid.uuid1(),
                      create_time=now, edit_time=now, show_time=now+delta_time, public=public)
        msg.save()
        return JsonResponse({
            'code': 200,
            'msg': ['Create message successfully']
        })


class MessageDetailView(View):
    http_method_names = ['get', 'put', 'delete']

    def get(self, request, uuid):
        if not uuid:
            return JsonResponse({
                'code': 404,
                'msg': ['Message not found']
            })
        try:
            message = Message.objects.get(uuid=uuid)
            if (not message.user == request.user) and (message.public == False):
                return JsonResponse({
                    'code': 403,
                    'msg': ['Access denied']
                })

            return JsonResponse({
                'code': 200,
                'content': model_to_dict(message, fields=['user', 'content', 'create_time', 'edit_time', 'show_time', 'pubilc', 'uuid'])
            })
        except ObjectDoesNotExist as e:
            return JsonResponse({
                'code': 404,
                'msg': ['Message not found']
            })

    def put(self, request, uuid):
        if not uuid:
            return JsonResponse({
                'code': 404,
                'msg': ['Message not found']
            })
        try:
            message = Message.objects.get(uuid=uuid)

            if (not message.user == request.user):
                return JsonResponse({
                    'code': 403,
                    'msg': ['Access denied']
                })

            delay_time = request.PUT.get('delay_time', '0:0:0:0')
            content = request.PUT.get('content', message.content)
            public = request.PUT.get('public', message.public)

            days, hours, minutes, seconds = list(
                map(int,
                    map(lambda x: x or 0,
                        re.findall(
                            '([0-9]+):([0-9]+):([0-9]+):([0-9]+)', delay_time)[0]
                        )
                    )
            )

            delta_time = datetime.timedelta(
                days=days,
                hours=hours,
                minutes=minutes,
                seconds=seconds
            )
            now = timezone.now()

            message.content = content
            message.edit_time = now
            message.show_time = now + delta_time
            message.pubilc = public

            message.save(update_fields=['content',
                                        'edit_time', 'show_time', 'public'])
            return JsonResponse({
                'code': 200,
                'msg': ['Edit successfully']
            })
        except ObjectDoesNotExist as e:
            return JsonResponse({
                'code': 404,
                'msg': ['Message not found']
            })

    def delete(self, request, uuid):
        if not uuid:
            return JsonResponse({
                'code': 404,
                'msg': ['Message not found']
            })
        try:
            message = Message.objects.get(uuid=uuid)

            if (not message.user == request.user):
                return JsonResponse({
                    'code': 403,
                    'msg': ['Access denied']
                })

            message.delete()
            return JsonResponse({
                'code': 200,
                'msg': ['Delete message successfully']
            })
        except ObjectDoesNotExist as e:
            return JsonResponse({
                'code': 404,
                'msg': ['Message not found']
            })


def create_json_ret(messages):
    content = [model_to_dict(m, fields=['user', 'content', 'edit_time', 'uuid'])
               for m in messages]
    return JsonResponse({
        'code': 200,
        'content': content
    })


class ShowMyMessageView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request):
        now = timezone.now()
        messages = request.user.message_set.filter(show_time__lt=now)

        return create_json_ret(messages)


class ShowMyAllMessageView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request):
        messages = request.user.message_set.all()

        content = [model_to_dict(m, fields=['user', 'content', 'edit_time', 'show_time', 'uuid'])
                   for m in messages]
        return JsonResponse({
            'code': 200,
            'content': content
        })


class ShowAllMessageView(View):
    http_method_names = ['get']

    def get(self, request):
        now = timezone.now()
        messages = request.user.message_set.filter(
            show_time__lt=now).filter(public=True)

        return create_json_ret(messages)
