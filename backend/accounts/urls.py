from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.backend_login, name='b_login'),
    path('logout/', views.backend_logout, name='b_logout'),
    path('register/', views.backend_register, name='b_register'),
    path('profile/show/', views.backend_profile_show, name='b_profile_show'),
    path('profile/edit/', views.backend_profile_edit, name='b_profile_edit'),
]
