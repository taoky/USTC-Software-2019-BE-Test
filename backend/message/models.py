from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_time = models.DateTimeField(default=timezone.now)
    hidden_seconds = models.IntegerField(default=0)
    content = models.CharField(max_length=255)

    @property
    def recieved_time(self):
        return self.send_time + timezone.timedelta(seconds=self.hidden_time)
