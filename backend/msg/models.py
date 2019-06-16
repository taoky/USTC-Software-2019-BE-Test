from django.contrib.auth import get_user_model
from django.db import models
from django.forms.models import model_to_dict as origin_model_to_dict
from django.utils import timezone

User = get_user_model()


def model_to_dict(model_instance, fields):
    if 'user' in fields:
        del fields[fields.index('user')]
        ret = origin_model_to_dict(model_instance, fields)
        ret.update({'user': model_instance.user.username})
        return ret
    else:
        return origin_model_to_dict(model_instance, fields)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()
    show_time = models.DateTimeField()
    public = models.BooleanField()
    uuid = models.UUIDField(unique=True)

    def is_showing(self):
        return self.show_time >= timezone.now()
