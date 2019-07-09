from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # In fact you can just attach email information in django User model.
    email = models.EmailField(blank=True)
    bio = models.CharField(max_length=50, blank=True)
    # Just to show it works.
    # More?

    def __str__(self):
        return self.user.username

