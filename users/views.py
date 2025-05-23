from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from acl.mixins import PermissionMixin
from acl.rest_mixin import RestPermissionMixin
from .serializers import *
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileView(PermissionMixin,RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(PermissionMixin,UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()


class UserListView(PermissionMixin,generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer(many=True)},
        description="لیست کاربران را نمایش می‌دهد"
    )
    def get(self, request):
        return super().get(request)

    @extend_schema(
        request=UserCreateSerializer,
        responses={201: UserCreateSerializer},
        description="یک کاربر جدید ایجاد می‌کند"
    )
    def post(self, request):
        return super().post(request)


class UserCreateView(PermissionMixin,APIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['user_create']

    @extend_schema(
        request=UserCreateSerializer,
        responses={201: UserCreateSerializer},
        description="یک کاربر جدید ایجاد می‌کند"
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserCreateSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(PermissionMixin,generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        responses={200: UserSerializer},
        description="جزئیات یک کاربر خاص را نمایش می‌دهد"
    )
    def get(self, request, pk=None):
        return super().get(request, pk)


class UserUpdateView(PermissionMixin,APIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['user_edit']
    
    @extend_schema(
        request=UserUpdateSerializer,
        responses={200: UserUpdateSerializer},
        description="اطلاعات کاربر را به‌روزرسانی می‌کند"
    )
    def put(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "کاربر یافت نشد!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(PermissionMixin,APIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['user_delete']

    @extend_schema(
        responses={204: None},
        description="یک کاربر را حذف می‌کند"
    )
    def delete(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "کاربر یافت نشد!"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"detail": "کاربر با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)
