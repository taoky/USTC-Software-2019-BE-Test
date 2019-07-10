from django.urls import path
from . import views

app_name = 'message'
urlpatterns = [
    path('index/<slug:username>', views.index_view, name='index'),
    path('create/<slug:username>', views.create_view, name='create'),
]