from django.shortcuts import render, redirect
from .forms import *
from .models import *



def contactus(request):
    template = 'contact.html'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        context = {'test_form':form}
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            obj = ContactFormModel(name=name, phone=phone, message=message)
            obj.save()
            return redirect('/contact')   # --------------------------------- Need to import '''redirect''' aslo like '''render'''
        else:
            return redirect('/contact')
    else:
        form = ContactForm()
        context = {'test_form':form}
        return render(request, template, context=context)
