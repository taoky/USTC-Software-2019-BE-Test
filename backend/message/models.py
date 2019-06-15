from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    sent_time = models.DateTimeField(default=timezone.now())
    hidden_time = models.IntegerField(default=0)  # Hidden seconds
    content = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def conveyed_time(self):
        return self.send_time + timezone.timedelta(seconds=self.hidden_time)
