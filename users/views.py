from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import *
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

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


class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]

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


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer},
        description="جزئیات یک کاربر خاص را نمایش می‌دهد"
    )
    def get(self, request, pk=None):
        return super().get(request, pk)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

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


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

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
