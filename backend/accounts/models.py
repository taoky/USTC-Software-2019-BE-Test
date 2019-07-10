from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'auth_user'
