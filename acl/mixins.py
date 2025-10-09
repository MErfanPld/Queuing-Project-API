from rest_framework.permissions import BasePermission

class PermissionMixin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True

        if not hasattr(view, 'permissions'):
            return True

        user_perms = set(user.permissions.values_list('code', flat=True))
        for perm in view.permissions:
            if perm in user_perms:
                return True
        return False
