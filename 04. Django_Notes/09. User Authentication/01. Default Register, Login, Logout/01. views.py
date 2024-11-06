from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
               return redirect('dashboard')
        else:
            messages.info(request, 'Invalid password or username')
            return redirect(request.get_full_path()) # Need to return current URL cause next URL and normal URL are different
    else:
        template = 'login.html'
        return render(request, template)
    

def logout(request):
    auth.logout(request)
    return redirect('/')



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'This username has already taken')
                return redirect('register')
            elif User.objects.filter(email=email):
                messages.info(request,"This email has already taken")
                return redirect('register')
                
            else:
                user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
                user.save()
                messages.info(request, 'Successfully created account')
                return redirect('login')
        else:
            messages.info(request, "Password dosen't match")
            return redirect('register')
    else:
        template = 'register.html'
        return render(request, template)

# Showing all data, it can remind unauthority page before login and send the user targted page after login
@login_required(login_url='login/')  # login/  is the custom login URL path
def AllDataShow(request):
    all_data = WesiteModel.objects.all()
    template = 'all_data_show.html'
    context = {'all_data':all_data}
    return render(request, template, context=context)
    
# This way can not remind unauthority page before login 
def AllDataShow(request):
    if request.user.is_authenticated:
        all_data = WesiteModel.objects.all()
        template = 'all_data_show.html'
        context = {'all_data':all_data}
        return render(request, template, context=context)
    else:
        return redirect('login')

