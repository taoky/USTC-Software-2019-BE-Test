from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('regist/', views.regist),
    path('login/', views.login),
]
