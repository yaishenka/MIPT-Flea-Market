from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'email','password')}),

        ('Permissions', {'fields': ('is_superuser',)}),
    )

    search_fields =  ('username', 'email')
    ordering = ('username','email')

    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)