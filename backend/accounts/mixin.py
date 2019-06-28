from django.http import JsonResponse


class LoginRequiredMixin:
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
