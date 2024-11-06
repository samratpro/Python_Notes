from django.shortcuts import render
from .forms import *
from .models import *



def contactus(request):
    context={}
    if request.method == 'POST' and 'name' in request.POST and 'phone' in request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        message = request.POST['message']
        context['name'] = name
        context['phone'] = phone
        context['message'] = message
        obj = ContactFormModel(name=name, phone=phone, message=message)
        obj.save()

    template = 'contact.html'
    return render(request, template, context=context)