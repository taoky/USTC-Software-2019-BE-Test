from django.views.generic.base import View
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginView(View):
    http_method_names = ['post', 'get']

    def post(self, request):
        pass

    def get(self, requst):
        pass


class RegisterView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, requst):
        pass


class ProfileView(View):
    http_method_names = ['get']

    def get(self, request):
        pass


class UpdateProfileView(View):
    http_method_names = ['post']

    def post(self, request):
        pass


class LogoutView(View):
    http_method_names = ['post']

    def post(self, requst):
        pass
