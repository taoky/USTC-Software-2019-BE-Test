from django.urls import path

from message import views

app_name = 'message'
urlpatterns = [
    path('send/', views.message_send, name='send'),
    path('recieve/', views.message_recieve, name='recieve'),
]
