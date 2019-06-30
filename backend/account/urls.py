from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('regist/', views.regist),
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile_show/', views.profile_show),
    path('profile_update/', views.profile_update),
    path('message_create/', views.message_create),
    path('message_show/', views.message_show),
    path('message_delete/', views.message_delete),
]
