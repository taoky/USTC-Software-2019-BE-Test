import datetime
import re

from django.http import JsonResponse
from django.utils import timezone
from django.views.generic.base import View

from msg.models import Message

from accounts.Mixin import LoginRequiredMixin


class CreateMessage(LoginRequiredMixin, View):
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

        msg = Message(user=request.user, content=content,
                      create_time=now, show_time=now+delta_time, public=public)
        msg.save()
        return JsonResponse({
            'code': 200,
            'msg': ['Create message successfully']
        })


class ShowMyMessage(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request):
        now = timezone.now()
        messages = request.user.message_set.filter(show_time__gt=now)

        content = [{'content': m.content,
                    'create_time': m.create_time,
                    'author': m.user
                    }
                   for m in messages]
        return JsonResponse({
            'code': 200,
            'content': content
        })


class ShowAllMessage(View):
    http_method_names = ['get']

    def get(self, request):
        now = timezone.now()
        messages = request.user.message_set.filter(
            show_time__gt=now).filter(public=True)

        content = [{'content': m.content,
                    'create_time': m.create_time,
                    'author': m.user
                    }
                   for m in messages]
        return JsonResponse({
            'code': 200,
            'content': content
        })
