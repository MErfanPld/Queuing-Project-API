from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from datetime import timedelta
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# from Auth.models import Code

class PermissionMixin(APIView):
    permission_classes = [IsAuthenticated]
    user = None
    permissions = []

    def check_permissions(self, request):
        self.user = request.user

        # Superuser bypass
        if self.user.is_superuser:
            return True

        # Staff users bypass
        if self.user.is_staff:
            return True

        # Custom permissions check
        if hasattr(self.user, 'permissions'):
            for permission in self.permissions:
                if permission in self.user.permissions:
                    return True

        return False

    def check_active(self, request):
        return self.user.is_active

    def handle_request(self, request, *args, **kwargs):
        # Check if user is active
        if not self.check_active(request):
            return Response({'detail': 'Account is inactive.'}, status=status.HTTP_403_FORBIDDEN)

        # Check permissions
        if not self.check_permissions(request):
            return Response({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

        return super().dispatch(request, *args, **kwargs)


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class AnonymousUserMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('users-list'))
        else:
            return super().dispatch(request, *args, **kwargs)


class VerifiedUserMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('login'))


# class CheckPasswordResetExpirationMixin:
#     def dispatch(self, request, *args, **kwargs):
#         if request.session.has_key('reset_password_code'):
#             reset_password = Code.objects.filter(code=request.session['reset_password_code']).first()
#             if reset_password:
#                 today = timezone.now()
#                 expiration = reset_password.created_at + timedelta(minutes=15)
#                 if today < expiration:
#                     return super().dispatch(request, *args, **kwargs)
#
#         try:
#             del request.session['reset_password_code']
#         except:
#             pass
#         return redirect('/')
