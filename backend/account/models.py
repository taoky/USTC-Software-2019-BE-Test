from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User_Info(AbstractUser):
    """
        message, release_time, wait_time, show_time and message_id are used for the optional mission,
        wait_time adn message_id should be an integer,
        release_time and show_time are planned to use the time from system.
    """
    profile = models.CharField(max_length=100, blank=True)
    message = models.CharField(max_length=100, blank=True)
    release_time = models.CharField(max_length=50)
    wait_time = models.CharField(max_length=10)
    show_time = models.CharField(max_length=50)
