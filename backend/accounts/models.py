from django.db import models
from django.contrib.auth.models import AbstractUser

password_strength = {
    'min_length': 8,
    'upper': True,
    'lower': True,
    'num': True,
    'symbol': True
}


class User(AbstractUser):
    nickname = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'auth_user'
