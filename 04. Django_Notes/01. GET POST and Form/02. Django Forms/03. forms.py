# In App Folder
from django import forms
from django.forms import TextInput, EmailInput

class ContactForm(forms.Form):
    name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    phone = forms.CharField(widget=TextInput(attrs={'placeholder': 'Phone', 'style': 'width: 300px;', 'class': 'form-control'}))
    message = forms.CharField(widget=TextInput(attrs={'placeholder': 'Message', 'style': 'width: 300px;', 'class': 'form-control', 'rows':'5'}))

