from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.backend_login, name='login'),
    path('logout/', views.backend_logout, name='logout'),
    path('register/', views.backend_register, name='register'),
    path('profile/', views.backend_profile, name='profile'),
]
