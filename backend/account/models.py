from django.db import models
from django import forms

gender = (
        ('male','男'),
        ('female','女'),
        ('unknown','未知'),
    )

class User(models.Model):
    name = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=16)
    sex = models.CharField(max_length=10,choices=gender,default='male')
    email = models.CharField(max_length=256,blank=True)

    def __str__(self):
        return self.name

class RegisterForm(forms.Form):
    
    username = forms.CharField(max_length=100,label='name',strip=True)
    password = forms.CharField(max_length=16,label='password')
    repassword = forms.CharField(max_length=16,label='password')
    sex = forms.ChoiceField(choices=gender,label='sex')
    email = forms.EmailField(label='email')

class LoginForm(forms.Form):

    username = forms.CharField(max_length=100,label='name',strip=True)
    password = forms.CharField(max_length=16,label='password')

class UpdateForm(forms.Form):

    re_new_password = forms.CharField(max_length=16,label='password')
    new_password = forms.CharField(max_length=16,label='repassword')
    new_sex = forms.ChoiceField(choices=gender,label='sex')
    new_email = forms.EmailField(label='email')

# Create your models here.
