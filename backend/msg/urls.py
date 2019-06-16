from django.urls import path

from django.contrib.auth import views as auth_views
from msg import views

app_name = 'msg'
urlpatterns = [
    path('create', views.CreateMessageView.as_view(), name='create_message'),
    path('my', views.ShowMyMessageView.as_view(), name='my_message'),
    path('my/all', views.ShowMyAllMessageView.as_view(), name='my_all_message'),
    path('', views.ShowAllMessageView.as_view(), name='all_message'),
    path('<uuid:uuid>/detail', views.MessageDetailView.as_view(),
         name='message_detail'),
    path('<uuid:uuid>/edit', views.MessageDetailView.as_view(), name='edit_message'),
]
