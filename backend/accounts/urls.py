from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.backend_login, name='login'),
    path('logout/', views.backend_logout, name='logout'),
    path('register/', views.backend_register, name='register'),
    path('profile/show/', views.backend_profile_edit, name='profile_edit'),
    path('profile/edit/', views.backend_profile_show, name='profile_show'),
]
