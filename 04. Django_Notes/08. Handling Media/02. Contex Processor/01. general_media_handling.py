'''
❌ For Logo and Icon we need to use ` context_processors `  ❌ 
❌ Cause Logo and Icon server each pages  ❌ 
❌ And in every function we need pass logo as context, that is painful, so we can use  ` context_processors ` ❌ 
'''


#  Admin.py ................................... 📄
from django.contrib import admin
from .models import *
admin.site.register(Logo)

# apps urls.py ................................ 📄
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.dashboard, name='dashboard'),  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # ************************


# models.py .................................... 📄
rom django.db import models
class Logo(models.Model):
    logo_img = models.ImageField(upload_to='images/')
    icon_img = models.ImageField(upload_to='images/')
    def __str__(self):
        return 'Logo'

# setting.py .................................. 📄

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                 '..............',
                'dashapp.logo_processors.logo_context',   # ******************************
            ],
        },
    },
]

# Need to create folder
# 🔽 media
#   ▶️ images 

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# views.py .................................. 📄
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Logo

@login_required(login_url='login/')
def dashboard(request):
    logos = Logo.objects.first()
    template = 'dashboard/dashboard.html'
    context = {'logos':logos}
    return render(request, template, context)


# base.html  ............................... 📄
<head>
  <link rel="shortcut icon" type="image/png" href="{{logos.icon_img.url}}" />     # ..... For icon
</head>

# dasbboard.html ........................... 📄
<img src="{{logos.logo_img.url}}" width="180" alt="" />                          # ---------- Logo 
