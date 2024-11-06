from django.contrib import admin
from .models import *                # or from .models import "ModuleName" 


# Add the field to make read-only
class ApiListAdmin(admin.ModelAdmin):
    readonly_fields = ('filled_quota',)  
admin.site.register(ApiList, ApiListAdmin)


# Register your models here.
admin.site.register(Module_Name) 

# Changing the Django Admin Header Text
admin.site.site_header = 'Project Name'    


""" Customize admin field with section """
from .models import ModelName

class CustomField(admin.ModelAdmin):
    list_display = ('field_name1', 'field_name2')   # Fields to show in list view
    list_filter = ('field_name1', 'field_name2')    # Optional: Add filters to filter by these fields
    search_fields = ('field_name1', 'field_name2', 'user__email')  # For search filter
    ''' field_name__related_field_name, user__email   : here uses  __ for Forigen Model field'''
    fieldsets = (
        ("Section Name", {
            'fields': ('field_name1', 'field_name2'),
            'description': 'Description Text',
        }),
        ('Section Name', {
            'fields': ('field_name3', 'field_name4'),
            'description': 'Description Text',
        }),
    )

admin.site.register(ModelName, CustomField)

