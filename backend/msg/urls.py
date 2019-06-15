from django.urls import path

from django.contrib.auth import views as auth_views
from msg import views

app_name = 'msg'
urlpatterns = [
    path('create', views.CreateMessage.as_view(), name='create_message'),
    path('my', views.ShowMyMessage.as_view(), name='my_message'),
    path('all', views.ShowAllMessage.as_view(), name='all_message')
]
