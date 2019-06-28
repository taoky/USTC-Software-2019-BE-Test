import datetime
import re
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic.base import View

from accounts.mixin import LoginRequiredMixin
from msg.models import Message

from .models import model_to_dict


class CreateMessageView(LoginRequiredMixin, View):
    '''
    处理用户创建消息的请求
    '''
    http_method_names = ['post']

    def post(self, request):
        '''
        处理用户对于```/msg/create```的post请求
        为用户创建一条新的消息

        @param in POST
            content<str>:  消息内容
            public<str>:  消息是否公开
            delay_time<str>:  延迟发布时间，格式：DD:HH:MM:SS

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义     |
                       | ------ | -------- |
                       | 200    | 创建成功 |
                       | 401    | 未登录   |
            msg<dict>:  返回代码相应的解释
        '''
        delay_time = request.POST.get('delay_time', '0:0:0:0')
        content = request.POST.get('content', '')
        public = request.POST.get('public', False) in (True, 'True')

        try:
            # 提交上来的延迟时间格式化为天、小时、分钟、秒
            # 提交的延迟时间格式为DD:HH:MM:SS
            days, hours, minutes, seconds = list(
                map(int,
                    map(lambda x: x or 0,
                        re.findall(
                            '^([0-9]+):([0-9]+):([0-9]+):([0-9]+)$', delay_time)[0]
                        )
                    )
            )
        except (IndexError, ValueError):
            # IndexError用于处理格式不正确的情况，即延迟时间中没有三个":"
            # ValueError用于处理冒号之间的内容不是数字或者缺省的情况
            return JsonResponse({
                'code': 410,
                'msg': [_('Incorrect delay_time format')]
            })

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
            'msg': [_('Create message successfully')]
        })


class MessageDetailView(LoginRequiredMixin, View):
    '''
    返回一条消息的详细信息
    处理用户的put、delete请求，用于更新消息以及删除消息
    '''
    http_method_names = ['get', 'put', 'delete']
    login_required_method = ['delete', 'put']

    def get(self, request, uuid):
        '''
        处理用户对于```/msg/<uuid>```的get请求
        返回uuid为<uuid>的消息的详细信息

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义     |
                       | ------ | -------- |
                       | 200    | 获取成功 |
                       | 401    | 未登录   |
            content<dcit>:  内容如下
                       | 参数名称    | 类型 | 描述           |
                       | ----------- | ---- | -------------- |
                       | content     | str  | 消息的内容     |
                       | create_time | str  | 创建时间       |
                       | edit_time   | str  | 修改时间       |
                       | show_time   | str  | 展示时间       |
                       | user        | str  | 作者           |
                       | public      | bool | 是否公开       |
                       | uuid        | str  | 这条消息的uuid |
        '''
        if not uuid:
            return JsonResponse({
                'code': 404,
                'msg': [_('Message not found')]
            })
        try:
            message = Message.objects.get(uuid=uuid)
            if (not message.user == request.user) and (message.public == False):
                return JsonResponse({
                    'code': 403,
                    'msg': [_('Access denied')]
                })

            return JsonResponse({
                'code': 200,
                'content': model_to_dict(message, fields=['user', 'content', 'create_time', 'edit_time', 'show_time', 'pubilc', 'uuid'])
            })
        except ObjectDoesNotExist as e:
            return JsonResponse({
                'code': 404,
                'msg': [_('Message not found')]
            })

    def put(self, request, uuid):
        '''
        处理用户对于```/msg/<uuid>```的put请求
        修改uuid为<uuid>的消息的详细信息

        @param in POST
            content<str>:  消息内容
            public<bool>:  消息是否公开
            delay_time<str>:  消息的延迟发布时间，格式：DD:HH:MM:SS

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义               |
                       | ------ | ------------------ |
                       | 200    | 修改成功           |
                       | 401    | 未登录             |
                       | 403    | 不是这条消息的作者 |
                       | 404    | 输入的uuid有误     |
            msg<dict>:  返回代码相应的解释
        '''
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
                    'msg': [_('Access denied')]
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
                'msg': [_('Edit message successfully')]
            })
        except ObjectDoesNotExist as e:
            return JsonResponse({
                'code': 404,
                'msg': [_('Message not found')]
            })

    def delete(self, request, uuid):
        '''
        处理用户对于```/msg/<uuid>```的delete请求
        删除uuid为<uuid>的消息

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义               |
                       | ------ | ------------------ |
                       | 200    | 修改成功           |
                       | 401    | 未登录             |
                       | 403    | 不是这条消息的作者 |
                       | 404    | 输入的uuid有误     |
            msg<dict>:  返回代码相应的解释
        '''
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
                    'msg': [_('Access denied')]
                })

            message.delete()
            return JsonResponse({
                'code': 200,
                'msg': [_('Delete message successfully')]
            })
        except ObjectDoesNotExist as e:
            return JsonResponse({
                'code': 404,
                'msg': [_('Message not found')]
            })


def create_json_ret(messages):
    '''
    将通过orm获取到的消息数据打包为JsonResponse返回

    @param
        messages:   所需要返回的消息数据

    @return in JsonResponse
        code<int>:  返回代码，恒为200
        content<list>:  所有消息组成的list，每个元素代表一条消息，按照时间降序排列
                        其中包含```user```，```content```，```edit_time```，```uuid```字段
    '''
    content = [model_to_dict(m, fields=['user', 'content', 'edit_time', 'uuid'])
               for m in messages]
    return JsonResponse({
        'code': 200,
        'content': content
    })


class ShowMyMessageView(LoginRequiredMixin, View):
    '''
    显示当前用户的所有可见消息
    **需要登录**
    '''
    http_method_names = ['get']

    def get(self, request):
        '''
        处理用户对于```/msg/my```的get请求
        返回当前用户的所有可见消息

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义     |
                       | ------ | -------- |
                       | 200    | 获取成功 |
                       | 401    | 未登录   |
            content<list>:  所有消息组成的list，每个元素代表一条消息，按照时间降序排列
                            其中包含```user```，```content```，```edit_time```，```uuid```字段
        '''
        now = timezone.now()
        messages = request.user.message_set.filter(
            show_time__lt=now).order_by('-show_time')

        return create_json_ret(messages)


class ShowMyAllMessageView(LoginRequiredMixin, View):
    '''
    显示当前用户的所有消息，包含未到展示时间的消息
    **需要登录**
    '''
    http_method_names = ['get']

    def get(self, request):
        '''
        处理用户对于```/msg/my/all```的get请求
        返回当前用户的所有消息

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义     |
                       | ------ | -------- |
                       | 200    | 获取成功 |
                       | 401    | 未登录   |
            content<list>:  所有消息组成的list，每个元素代表一条消息，按照时间降序排列
                            其中包含```user```，```content```，```edit_time```，```show_time```，```uuid```字段
        '''
        messages = request.user.message_set.all().order_by('-show_time')

        content = [model_to_dict(m, fields=['user', 'content', 'edit_time', 'show_time', 'uuid'])
                   for m in messages]
        return JsonResponse({
            'code': 200,
            'content': content
        })


class ShowAllMessageView(View):
    '''
    显示所有用户的公开可见消息
    '''
    http_method_names = ['get']

    def get(self, request):
        '''
        处理用户对于```/msg/all```的get请求
        返回所有用户的公开可见消息

        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       | 返回值 | 含义     |
                       | ------ | -------- |
                       | 200    | 获取成功 |
                       | 401    | 未登录   |
            content<list>:  所有消息组成的list，每个元素代表一条消息，按照时间降序排列
                            其中包含```user```，```content```，```edit_time```，```uuid```字段
        '''
        now = timezone.now()
        messages = request.user.message_set.filter(
            show_time__lt=now).filter(public=True).order_by('-show_time')
        return create_json_ret(messages)
