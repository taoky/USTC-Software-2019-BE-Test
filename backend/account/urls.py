from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('regist/', views.regist),
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile_show/', views.profile_show),
    path('profile_update/', views.profile_update),
]
