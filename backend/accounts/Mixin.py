from django.http import JsonResponse


class LoginRequiredMixin:
    '''
    要求用户登陆的mixin
    在子类中重写login_required_method，以定义哪些请求需要进行登录控制
        若未重写login_required_method，则所有类型的请求都将需要登录
    '''
    login_required_method = ['get', 'post', 'put',
                             'patch', 'delete', 'head', 'options', 'trace']

    def dispatch(self, request, *args, **kwargs):
        if (request.method.lower() in self.login_required_method) and (not request.user.is_authenticated):
            return JsonResponse({
                'code': 401,
                'msg': ['Please log in first']
            })
        else:
            return super().dispatch(request, *args, **kwargs)
