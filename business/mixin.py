from rest_framework.exceptions import PermissionDenied
from .models import Business


class BusinessContextMixin:
    def get_business(self):
        if self.request.user.is_superuser:
            return None

        if not hasattr(self.request.user, 'business'):
            raise PermissionDenied("شما کسب‌وکار ندارید")

        business = self.request.user.business
        if not business.is_active:
            raise PermissionDenied("کسب‌وکار غیرفعال است")

        return business
