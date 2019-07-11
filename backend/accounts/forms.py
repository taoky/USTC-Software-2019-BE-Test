from django import forms

from .models import Detail, Information

class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['text']
        labels = {'text': ''}

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
