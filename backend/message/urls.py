from django.urls import path
from . import views

app_name = 'message'
urlpatterns = [
    path('<slug:username>/', views.index_view, name='index'),
    path('<slug:username>/create', views.create_view, name='create'),
]