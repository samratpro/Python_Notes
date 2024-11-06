python manage.py shell

>>>  from django.contrib.auth.models import User                    // For Auth User
>>>  from userapp.models import AppUser                             // ` userapp ` is App Name & ` AppUser ` is Custom user model name
>>>  user = AppUser.objects.get(email="nichescl@gmail.com")         //  Filtering by email
>>>  user.set_password("admin")
>>>  user.save()
