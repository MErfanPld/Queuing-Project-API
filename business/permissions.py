from rest_framework.permissions import BasePermission, SAFE_METHODS
from business.models import Business

# ==========================
# دسترسی بر اساس نقش
# ==========================

class IsAdmin(BasePermission):
    """فقط ادمین دسترسی دارد"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsBusinessOwner(BasePermission):
    """فقط صاحب کسب‌وکار دسترسی دارد"""
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            Business.objects.filter(owner=request.user).exists()
        )


class IsCustomer(BasePermission):
    """فقط مشتری (نه ادمین و نه صاحب کسب‌وکار)"""
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            not request.user.is_superuser and
            not Business.objects.filter(owner=request.user).exists()
        )


# ==========================
# دسترسی بر اساس شیء (Object)
# ==========================

class IsOwnerOfBusiness(BasePermission):
    """فقط صاحب آن کسب‌وکار روی شیء دسترسی دارد"""
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.owner == request.user or request.user.is_superuser
        )


class IsOwnerOfObject(BasePermission):
    """
    دسترسی روی شیء (obj) که attribute `business` دارد.
    ادمین همه چیز را می‌تواند ببینید.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return hasattr(obj, 'business') and obj.business.owner == request.user


# ==========================
# ترکیبی
# ==========================

class IsAdminOrBusinessOwner(BasePermission):
    """ادمین یا صاحب کسب‌وکار روی شیء"""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return hasattr(obj, 'business') and obj.business.owner == request.user


class IsBusinessOwnerOrAdmin(BasePermission):
    """دسترسی به تمام عملیات: ادمین یا صاحب کسب‌وکار"""
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            (request.user.is_superuser or Business.objects.filter(owner=request.user).exists())
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return hasattr(obj, 'business') and obj.business.owner == request.user


# ==========================
# حالت فقط خواندنی برای مشتری
# ==========================

class ReadOnlyForCustomer(BasePermission):
    """
    مشتری فقط GET/HEAD/OPTIONS می‌تواند ببیند.
    صاحب کسب‌وکار و ادمین تمام دسترسی‌ها را دارند.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and
            (request.user.is_superuser or Business.objects.filter(owner=request.user).exists())
        )
