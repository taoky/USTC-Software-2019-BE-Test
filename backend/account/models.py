from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User_Info(AbstractUser):
    profile = models.CharField(max_length=100, blank=True)
