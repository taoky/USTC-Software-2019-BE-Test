from django import forms
from .models import UserPro
from django.contrib.auth.models import User


class RegisForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Pssword", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']


class UserProForm(forms.ModelForm):
    class Meta:
        model = UserPro
        fields = ('phone', 'company', 'selfpro')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
