import json

from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class JSONParsingMiddleware(MiddlewareMixin):
    '''
    将PUT请求中的数据解析为json，保存到request.PUT中

    Django中默认只将GET和POST请求中的数据进行json解析，存放到request.GET和request.POST中
    '''
    def process_request(self, request):
        if request.method == 'PUT':
            if request.content_type == 'application/json':
                try:
                    request.PUT = json.loads(request.body)
                except ValueError as e:
                    return JsonResponse({
                        'code': 400,
                        'msg': ['Can not parse the json', str(e)]
                    })
            else:
                return JsonResponse({
                    'code': 400,
                    'msg': ['PUT method require content_type="application/json" in header']
                })
