"""为应用程序users定义URL模式"""

from django.conf.urls import url
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    # 登录页面
    url(r'^login/$', views.login, name='login'),
    # 注销
    url(r'^logout/$', views.logout_view, name='logout'),
    # 注册页面
    url(r'^register/$', views.register, name='register'),
]