from django.urls import path

from . import views

app_name = 'message'
urlpatterns = [
    path('send/', views.message_send, name='message_send'),
    path('recieve/', views.message_recieve, name='message_recieve'),
]
