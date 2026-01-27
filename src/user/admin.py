from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.api.v1.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for custom User model."""
    
    list_display = ('id_user', 'username', 'email', 'role', 'first_name', 'last_name', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone_number')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'email', 'phone_number')
        }),
    )
