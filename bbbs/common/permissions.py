from rest_framework import permissions
from django.contrib.admin import ModelAdmin


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    Base permission for models with author
    """

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    # Deny permission for regional moderator
    def has_object_permission(self, request, view, obj):
        if view.action in ['partial_update', 'update']:
            return (
                    obj.author == request.user
                    or request.user.is_admin
                    or request.user.is_moderator
            )
        return True


class BaseStaffAdminPermission(ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    # Reg-moderator can not delete content
    # Except for places and events in his region
    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin or request.user.is_moderator:
            return True
        if request.user.is_moderator_reg and (
                self.model.__name__ == 'Place' or self.model.__name__ == 'Event'
        ):
            return True
        return False
