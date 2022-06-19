from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ('email', 'name', 'phone_number', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'phone_number')

    fieldsets = (
        (None, {'fields': ('name', 'phone_number', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        (('Important dates'), {'fields': ('last_login',)}),        
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )
        

admin.site.register(models.User, UserAdmin)
