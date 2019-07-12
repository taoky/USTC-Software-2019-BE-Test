"""定义accounts的URL模式"""
from django.conf.urls import url

from . import views

urlpatterns = [
    #主页
    url(r'^$', views.index, name='index'),

    #显示所有个人信息名称
    url(r'^details/$', views.details, name='details'),

    #显示特定信息细节
    url(r'^details/(?P<detail_id>\d+)/$', views.detail, name= 'detail'),

    #用于添加新信息名称的网页
    url(r'^new_detail/$', views.new_detail, name='new_detail'),

    #用于添加新信息的页面
    url(r'^new_information/(?P<detail_id>\d+)/$', views.new_information, name='new_information'),

    #用于编辑信息的页面
    url(r'^edit_information/(?P<information_id>\d+)/$', views.edit_information, name='edit_information')
]