from django.http import JsonResponse


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'code': 401,
                'msg': ['Please log in first']
            })
        else:
            return super().dispatch(request, *args, **kwargs)
