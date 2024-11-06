from django import forms
from django.forms import TextInput

class DataForms(forms.Form):
    data_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Website Name', 'class': 'form-control mb-3 mt-3'}))
    data_url = forms.URLField(widget=TextInput(attrs={'placeholder': 'Website URL', 'class': 'form-control mb-3'}))
