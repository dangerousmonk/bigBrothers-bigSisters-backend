from django.apps import apps
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ( "username", "city", 'gender')}),
        (_("Extra info"), {"fields": ("role",)}),
        (_("Permissions"), {"fields": ("is_active", "is_superuser")}),
    )



admin.site.register(CustomUser, UserAdmin)