from django.http import JsonResponse
from django.shortcuts import render
from requests import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import *

from acl.permissions import PERMISSIONS, filter_permissions

from .models import *
from .serializer import *

# Create your views here.


class RoleAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class PermissionsAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class UserPermissionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserWithPermissionsSerializer

    def get_queryset(self):
        return UserPermission.objects.select_related('user').prefetch_related('permissions')


class UserPermissionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer


class UserPermissionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except UserPermission.DoesNotExist:
            return Response({'detail': 'دسترسی کاربر پیدا نشد.'}, status=status.HTTP_404_NOT_FOUND)


class UserRoleAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserRole.objects.all()
    serializer_class = Role_UserSerializer