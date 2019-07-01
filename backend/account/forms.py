from django import forms
from .models import User_Info

#Learning this method from CSDN

class RegistrationForm(forms.Form):
    """
        Registration needs a format to strict: username, password, profile.
    """
    username = forms.CharField(label='', max_length=100, required=False)
    password = forms.CharField(label='', widget=forms.PasswordInput, required=False)
    password_re = forms.CharField(label='', widget=forms.PasswordInput, required=False)
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
            raise forms.ValidationError("004,Your password must be longer than 6 words.")
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
                raise forms.ValidationError("005,Your password must contain numbers.")

    def clean_password_re(self):
        password = self.cleaned_data.get('password')
        password_re = self.cleaned_data.get('password_re')
        if password_re != password:
            raise forms.ValidationError("006,Two passwords mismatch. Please try again.")
        else:
            return password_re

    def clean_profile(self):
        profile = self.cleaned_data.get('profile')
        if profile == None:
            profile = ''
        if len(profile) > 70:
            raise forms.ValidationError("007,Your profile must be shorter than 70 words.")
        else:
            return profile


class MessageForm(forms.Form):
    """
        Message needs a format to restrict: wait_time, message_id.
    """
    wait_time = forms.CharField(label='', max_length=10, required=False)
    username = forms.CharField(label='', max_length=100, required=False)
    
    def clean_wait_time(self):
        """
            Wait_time must be a nonnegative integer.
        """
        wait_time_str = self.cleaned_data.get('wait_time')
        if len(wait_time_str) == 0:
            raise forms.ValidationError("501,You must write a nonnegative integer wait_time.")
        else:
            try:
                wait_time = float(wait_time_str)
            except:
                raise forms.ValidationError("502,Your wait_time must be a nonnegative integer.")
            if not wait_time.is_integer():
                raise forms.ValidationError("502,Your wait_time must be a nonnegative integer.")
            else:
                wait_time = int(wait_time)
                if wait_time < 0:
                    raise forms.ValidationError("502,Your wait_time must be a nonnegative integer.")
                else:
                    return wait_time

    def clean_username(self):
        """
            Same as wait_time.
            Save message_id as username.
            Message_id and username won't conflict with each other, because the length of the real username is restrict to be longer than 3.
        """
        message_id_str = self.cleaned_data.get('username')
        if len(message_id_str) == 0:
            raise forms.ValidationError("503,You must write a nonnegative integer message_id.")
        else:
            try:
                message_id = float(message_id_str)
            except:
                raise forms.ValidationError("504,Your message_id must be a nonnegative integer.")
            if not message_id.is_integer():
                raise forms.ValidationError("504,Your message_id must be a nonnegative integer.")
            else:
                message_id = int(message_id)
                if message_id < 0:
                    raise forms.ValidationError("504,Your message_id must be a nonnegative integer.")
                elif message_id > 99:
                    raise forms.ValidationError("506,Your message_id must be smaller than 100, please delete some messages.")
                else:
                    checkresult = User_Info.objects.filter(username=str(message_id))
                    if len(checkresult) > 0:
                        raise forms.ValidationError("505,Your message_id already exists, please change another one.")
                    else:
                        return message_id
