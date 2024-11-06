# admin.py
from django.contrib import admin
from .models import NavigationItem

class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    ordering = ('order',)

admin.site.register(NavigationItem, NavigationItemAdmin)
