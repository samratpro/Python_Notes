from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ContactFormModel)


admin.site.site_header = 'Simple Blog'  