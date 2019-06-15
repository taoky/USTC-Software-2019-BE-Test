from django.urls import path

from django.contrib.auth import views as auth_views
from . import views
app_name = 'accounts'

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('register', views.RegisterView.as_view()),
    path('profile', views.ProfileView.as_view()),
    path('update_profile', views.UpdateProfileView.as_view()),
]
