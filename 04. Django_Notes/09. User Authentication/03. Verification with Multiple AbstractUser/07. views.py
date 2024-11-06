from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AppUser                                  # Custom User from Model
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
def logout(request):
    auth.logout(request)
    return redirect('/')


# Register account
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_type = request.POST['user_type']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 and password1 == password2:
            if AppUser.objects.filter(email=email):
                messages.info(request,"This email has already taken")
                return redirect('register')  
            else:
                if user_type == 'teacher':
                    user = AppUser.objects.create_teacher(is_active=False, email=email, password=password1, first_name=first_name, last_name=last_name)
                    user.save()
                else:
                    user = AppUser.objects.create_student(is_active=False, email=email, password=password1, first_name=first_name, last_name=last_name)
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
    



@login_required(login_url='login')
def profile(request):
    user_profile = AppUser.objects.get(email=request.user.email)
    if request.method == 'POST':
        profile_image = request.FILES.get('img_upload')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if first_name:
            user_profile.first_name = first_name
            user_profile.save()
        if last_name:
            user_profile.last_name = last_name
            user_profile.save()
        if email:
            user_profile.email = email
            user_profile.save()
        if password1 and password1 == password2:
            user_profile.set_password(password1)
            user_profile.save()
        if profile_image:
            user_profile.profile_image = profile_image
            user_profile.save()
        return redirect('profile')
    return render(request, 'user/profile/profile.html', {'user_profile': user_profile})



#  If task
'''
from .models Task 
def dashboard(request):
    if request.user.is_teacher:
        # Display teacher dashboard
        tasks = Task.objects.filter(assigned_to=request.user)
    elif request.user.is_student:
        # Display student dashboard
        tasks = Task.objects.filter(assigned_to=request.user)
    else:
        # Handle other user types
        tasks = []

    return render(request, 'dashboard.html', {'tasks': tasks})

'''

'''
@login_required
def remove_student(request, student_id):
    # Check if the user is a teacher
    user_profile = get_object_or_404(AppUser, user=request.user)
    if not user_profile.teachers.exists():
        return redirect('profile')  # Redirect to the profile page if not a teacher

    student = get_object_or_404(AppUser, id=student_id)

    # Check if the student is one of the teacher's students
    if student in user_profile.students.all():
        # Remove the student from the teacher's list of students
        user_profile.students.remove(student)
        return redirect('profile')  # Redirect to the profile page
    else:
        return redirect('profile')  # Redirect to the profile page if the student is not a student of the teacher

'''
