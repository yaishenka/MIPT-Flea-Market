from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_active', 'is_verified')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'email','password', 'groups')}),

        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_verified')}),
    )

    search_fields =  ('username', 'email')
    ordering = ('username','email')

    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)