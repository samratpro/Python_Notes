from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *  # Replace with your custom user model

# admin.site.register(AppUser)

# Changing the Django Admin Header Text
admin.site.site_header = 'Project Name'   


# Custom Admin View for User Management
# Included password Reset Fields
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('activation_code', 'password_reset_code', 'profile_image', 'credit', 'thread' ,'expire_date', 'credit_package')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # *********** Purchase by Admin ****************
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Check if a credit package is selected and update user's credit accordingly
        selected_package = form.cleaned_data.get('credit_package')
        if selected_package:
            obj.purchase_credit(selected_package)

    # *************** Credit expiration check from admin view ****************
    def changelist_view(self, request, extra_context=None):
        # Check credit expiration for all users
        users = AppUser.objects.all()
        for user in users:
            user.credit_expiration()
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(CreditPackage)
admin.site.register(PaddleToken)

