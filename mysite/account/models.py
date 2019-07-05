from django.db import models
from django.contrib.auth.models import User


class UserPro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=25, blank=True)
    selfpro = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)
    # Create your models here.
