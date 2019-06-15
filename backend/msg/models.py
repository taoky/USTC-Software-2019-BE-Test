from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()
    show_time = models.DateTimeField()
    public = models.BooleanField()
    uuid = models.UUIDField(unique=True, index=True)

    def is_showing(self):
        return self.show_time >= timezone.now()
