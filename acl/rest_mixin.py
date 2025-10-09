from rest_framework import permissions

class RestPermissionMixin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"🔍 Checking permissions for: {request.user}")

        if not request.user.is_authenticated:
            print("⛔ user not authenticated")
            return False

        if getattr(request.user, 'is_superuser', False):
            print("✅ superuser access granted")
            return True

        if not hasattr(view, 'permissions') or not view.permissions:
            print("ℹ️ no specific permissions required")
            return True

        # ✅ اگر permissions یک لیست ساده باشد
        user_permissions = set(request.user.permissions)

        print("👤 user permissions:", user_permissions)

        for perm in view.permissions:
            if perm in user_permissions:
                print(f"✅ permission granted: {perm}")
                return True

        print(f"⛔ access denied for {view.permissions}")
        return False
