import json

from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class JSONParsingMiddleware(MiddlewareMixin):
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
