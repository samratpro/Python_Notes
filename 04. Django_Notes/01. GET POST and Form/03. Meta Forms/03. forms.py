# In App Folder
# Meta Forms
from django import forms
from django.forms import TextInput, Textarea, EmailField, DateField    # all HTML fields has
from .models import ContactFormModel

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormModel
        fields = ['name', 'phone', 'message']

        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
            'phone': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Phone'
                }),
            'message': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Message',
                'rows':'5',
                'id':'comment',
                }),
        }


