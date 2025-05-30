from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AppUser                                    # Custom User from Model
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string


# Login
def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')   # ``dashboard`` path is destination
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                next_url = request.GET.get('next')  # `` Get next `` will grab next targeted URL, which page was requested by User that need to Login
                if next_url:
                    return redirect(next_url)
                else:
                   return redirect('dashboard')
            else:
                messages.info(request, 'Invalid password or username')
                return redirect(request.get_full_path()) # When fail to login, need to return current URL cause next URL and normal URL are different
        else:
            template = 'user/login_html/login.html'
            return render(request, template)


# Must be follow this function
@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('/login/')


# Register account
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 and password1 == password2:
            if AppUser.objects.filter(email=email):
                messages.info(request,"This email has already taken")
                return redirect('register')  
            else:
                user = AppUser.objects.create_user(is_active=False, email=email, password=password1, first_name=first_name, last_name=last_name)
                user.save()

                activation_code = get_random_string(30)
                user.activation_code = activation_code
                user.save()
                
                # Send activation email
                current_site = get_current_site(request)
                domain = current_site.domain
                from_email = 'noreply@mydomain.com'
                activation_link = f'{domain}/activate/{activation_code}/'
                send_mail(
                    'Activate Your Account',
                    f'Thank you for Registration, Following link to activate your account: {activation_link} \n Please don\'t share this link with any other',
                    from_email,
                    [email],
                    fail_silently=False
                )
                
                messages.info(request, 'Successfully created account')
                return redirect('login')
        else:
            messages.info(request, "Password dosen't match")
            return redirect('register')
    else:
        template = 'user/register_html/register.html'
        return render(request, template)



# Active Register account

def activate_account(request, activation_code):
    try:
        user = AppUser.objects.get(activation_code=activation_code, is_active=False)
    except AppUser.DoesNotExist:
        return render(request, 'user/register/activation_failed.html')
    user.activate()   # This activate() method come from AppUser class of the models.py
    return render(request, 'user/register/activation_success.html')




# When user forget password, sending reset code in mail

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = AppUser.objects.filter(email=email).first()

        if user:
            # Generate a password reset token and send it to the user via email
            forget_code = get_random_string(30)
            user.password_reset_code = forget_code
            user.save()
            
            protocol = 'https' if request.is_secure() else 'http'
            current_site = get_current_site(request)
            reset_url = f"{protocol}://{current_site.domain}/forget_password/confirm/{forget_code}/"
            subject = "Password Reset Request"
            message = f"Hello {user.first_name},\n\n"
            message += f"Click the following link to reset your password: {reset_url}"

            send_mail(subject, message, 'noreply@mydomain.com', [email], fail_silently=False)
            messages.success(request, 'We have sent you an email with instructions on how to reset your password.')
            return render(request, 'user/forget_password/send_code.html')
        else:
            messages.error(request, "This email doesn't exist")
            return render(request, 'user/forget_password/send_code.html')
    else:
        return render(request, 'user/forget_password/send_code.html')




# Set a new password 

def forget_password_confirm(request, forget_code):
    try:
        user = AppUser.objects.get(password_reset_code=forget_code, is_active=True)
        if user is not None:
            if request.method == 'POST':
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                if new_password1 and new_password1 == new_password2:
                    user.password_reset_code = ''
                    user.set_password(new_password1)
                    user.save()
                    return render(request, 'user/forget_password/password_reset_done.html')
                else:
                    messages.error(request, "Password Dosen't Match")
                    return render(request, 'user/forget_password/set_new_password.html')
            else:
                return render(request, 'user/forget_password/set_new_password.html')
        else:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('forget_password')
    except:
        return render(request, 'user/forget_password/password_reset_failed.html')



@login_required(login_url='/login/')
def setting(request):
    user = request.user

    if request.method == 'POST':
        # Handle Profile Settings Form
        if 'email' in request.POST:
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            try:
                # Validate email format
                validate_email(email)
                # Check if email is already taken by another user
                if AppUser.objects.filter(email__iexact=email).exclude(id=user.id).exists():
                    messages.error(request, 'This email is already in use.')
                else:
                    user.email = email.lower()
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    messages.success(request, 'Profile updated successfully.')
            except ValidationError:
                messages.error(request, 'Invalid email format.')

        # Handle Password Change Form
        elif 'current_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_new_password')

            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password) < 8:  # Basic password validation
                messages.error(request, 'New password must be at least 8 characters long.')
            else:
                user.set_password(new_password)
                user.save()
                # Keep user logged in after password change
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated successfully.')

        # Handle Notification Settings Form
        elif 'email_notifications' in request.POST:
            user.email_notifications = 'email_notifications' in request.POST
            user.device_login_alerts = 'device_login_alerts' in request.POST
            user.newsletter = 'newsletter' in request.POST
            user.save()
            messages.success(request, 'Notification settings updated successfully.')

    # Render the settings page with current user data
    context = {
        'user': user,
    }
    return render(request, 'sofmakeapp/settings.html', context)


