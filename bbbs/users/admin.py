from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class UserAdmin(DjangoUserAdmin):
    readonly_fields = ['date_joined', 'last_login']
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'city', 'is_staff', 'is_mentor', 'curator')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'city')
    fieldsets = (
        (_('Login/password'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', ('first_name', 'last_name'), 'city', 'gender', 'role', 'curator')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        (_('User activity'), {
            'classes': ('collapse',),
            'fields': ('date_joined', 'last_login',)
        }),
    )
    create_fieldsets = (
        (_('Login/password'), {'fields': ('email',)}),
        (_("Personal info"), {"fields": ('first_name', 'last_name', "city", 'gender', 'role', 'curator')}),
        (_("Permissions"), {"fields": ("is_active", "is_superuser", 'is_staff')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + create_fieldsets


admin.site.register(CustomUser, UserAdmin)
