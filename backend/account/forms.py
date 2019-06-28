from django import forms
from django.contrib.auth.models import User

#Learning this method from CSDN

class RegistrationForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password_re = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    #Use clean methods to restrict input values

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("Your username must be longer than 3 words.")
        elif len(username) > 20:
            raise forms.ValidationError("Your username must be shorter than 20 words.")
        else:
            #To check whether the username already exists
            checkresult = User.objects.filter(username=username)
            if len(checkresult) > 0:
                raise forms.ValidationError("Your username already exists.")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Your password must be longer than 6 words.")
        else:
            return password

    def clean_password_re(self):
        password = self.cleaned_data.get('password')
        password_re = self.cleaned_data.get('password_re')
        if password_re != password:
            raise forms.ValidationError("Two passwords mismatch. Please try again.")
        else:
            return password_re

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        checkresult = User.objects.filter(username=username)
        if not checkresult:
            raise forms.ValidationError("This username does not exist. Please try again.")
        else:
            return username


