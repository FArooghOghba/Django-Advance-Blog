from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile


# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'is_active', 'is_staff',
        'is_superuser', 'is_verified'
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_verified')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'is_verified')
        }),
        ('Group Permissions', {
            'fields': ('groups', 'user_permissions')
        }),
        ('Important Date', {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        ('Authentication', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'is_verified')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
