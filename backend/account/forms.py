from django import forms
from .models import User_Info

#Learning this method from CSDN

class RegistrationForm(forms.Form):
    """
        Only the registration need a format to strict.
    """
    username = forms.CharField(label='', max_length=100)
    password = forms.CharField(label='', widget=forms.PasswordInput)
    password_re = forms.CharField(label='', widget=forms.PasswordInput)
    profile = forms.CharField(label='', max_length=100, required=False)

    #Use clean methods to restrict input values

    def clean_username(self):
        """
            Username must be longer than 3 words and shorter than 20 words, no format restriction.
        """
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("001,Your username must be longer than 3 words.")
        elif len(username) > 20:
            raise forms.ValidationError("002,Your username must be shorter than 20 words.")
        else:
            #To check whether the username already exists
            checkresult = User_Info.objects.filter(username=username)
            if len(checkresult) > 0:
                raise forms.ValidationError("003,Your username already exists.")
        return username
    
    def clean_password(self):
        """
            Password must be longer than 6 words and must contain numbers.
        """
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("011,Your password must be longer than 6 words.")
        else:
            password_c = list(password)
            flag = 0
            for c in password_c:
                if ord(c) > 47 and ord(c) < 58:
                    flag = 1
                    break
            if flag == 1:
                return password
            else:
                raise forms.ValidationError("012,Your password must contain numbers.")

    def clean_password_re(self):
        password = self.cleaned_data.get('password')
        password_re = self.cleaned_data.get('password_re')
        if password_re != password:
            raise forms.ValidationError("013,Two passwords mismatch. Please try again.")
        else:
            return password_re

    def clean_profile(self):
        profile = self.cleaned_data.get('profile')
        if profile == None:
            profile = ''
        if len(profile) > 70:
            raise forms.ValidationError("021,Your profile must be shorter than 70 words")
        else:
            return profile

