from django.urls import path
from . import views


app_name = 'user_profile'
urlpatterns = [
    path('<slug:username>/edit', views.edit_view, name='edit'),
    path('<slug:username>/', views.index_view, name='index')
]