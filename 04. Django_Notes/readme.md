### 00. Env Setup
```basg
python -m venv env
source env/scripts/activate
```
### 01. Django install..
```bash
pip install django
```
### 01. Django Project Create..
```bash
django-admin startproject "projectname" .
django-admin startproject core .
```
### 02. Django App Creating..
```bash
python manage.py startapp "appname"
```
### 03. Server Running..
```bash
python manage.py runserver / python manage.py runserver 0.0.0.0:8000 --noreload
Ctrl + C   # server stop
```
### 04. For database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 05. Clean Migrations
File : .env
```
APPS=appname1 appname2 appname3
```
```
Then run clean.py exist in Additional Features Folder
Must clean migration if fail to update database
```
### 06. For Admin user creation
```bash
python manage.py createsuperuser
winpty python manage.py createsuperuser 
```
### 07. Important folders..
```
templates
static
🔽 media
   ▶️ images
🔽 logs
    console.log
```
### 08. Change in static folder
```
Need to run this command especially when application in server
```
```bash
python manage.py collectstatic
```
### 09. Image shows from static folder or database
```html
<img src="{% if request.user.profile_image %}{{request.user.profile_image.url}}{% else %}{% static "images/profile/user.png" %}{% endif %}" alt="" width="35" height="35" class="rounded-circle">
```

### 10. 404 Page
```
404.html and Debug is false for 404 page
```

### 11. CSS JS support
```html
{% load static %}
<link rel="stylesheet" href="{% static 'style.css' %}">
<script src="{% static 'myfirst.js' %}"></script>
```

### 12. Changing the Django Admin Credit (admin.py)
```py
#  admin.py in Registered last App in setting will get top priority
from django.contrib import admin
admin.site.site_title = "My Custom Admin Title"
admin.site.site_header = "My Custom Admin Portal"
admin.site.index_title = "Welcome to Admin Dashboard"
```
### 13. Changing the Django Admin Url (urls.py in project folder)
```py
from django.contrib import admin
urlpatterns = [
    path('custom-admin/', admin.site.urls),
] 
```
## 14. Django Architecture
```
.env
▶️ core
▶️ app1
▶️ app2
🔽 static
   ▶️ css
   ▶️ js
   ▶️ images
🔽 templates
   📄 base.html
   ▶️ app1
      📄 file.html
   ▶️ app2
      📄 file.html
🔽 media
   ▶️ images
🔽 logs
    console.log
clean.py
.env
manage.py
```
