from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('user_index',views.user_index,name='user_index'),
    path('update_user_index',views.update_user_index,name='update_user_index'),
]
