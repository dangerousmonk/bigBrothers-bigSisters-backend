from rest_framework import permissions


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
