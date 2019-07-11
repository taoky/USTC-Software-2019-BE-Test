from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_time = models.DateTimeField()
    available_time = models.DateTimeField()

    def __str__(self):
        if len(self.content) >= 15:
            return self.content[0:15] + '...'
        else:
            return self.content

