from django.db import models

class User(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
        ('unknown','不明'),
    )
    name = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=16)
    sex = models.CharField(max_length=10,choices=gender,default='male')
    email = models.CharField(max_length=256,blank=True)

    def __str__(self):
        return self.name



# Create your models here.
