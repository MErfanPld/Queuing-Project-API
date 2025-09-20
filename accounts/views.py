import random
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiExample

from accounts.models import OTP
from accounts.utils import send_otp_sms
from .serializers import LoginSerializer, RegisterSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from users.serializers import UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        self.token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': RegisterSerializer(user).data
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = self.token_data
        return response


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'شماره تلفن یا رمز عبور اشتباه است'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.data.get("refresh")
            if not token:
                return Response({"error": "توکن اجباری است"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken(token)

            # بررسی کن که آیا blacklist فعال است؟
            if hasattr(refresh, 'blacklist'):
                refresh.blacklist()

            return Response({"message": "خروج موفقیت‌آمیز بود"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: "پسورد با موفقیت تغییر کرد.", 400: "خطا در تغییر پسورد"},
        examples=[
            OpenApiExample(
                'مثال تغییر پسورد',
                value={
                    'old_password': 'oldpassword123',
                    'new_password': 'newpassword456',
                    'confirm_password': 'newpassword456'
                },
                request_only=True,
            )
        ]
    )
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # بررسی پسورد فعلی
            if not user.check_password(old_password):
                return Response({"detail": "پسورد فعلی صحیح نیست."}, status=status.HTTP_400_BAD_REQUEST)

            # تغییر پسورد
            user.set_password(new_password)
            user.save()
            return Response({"detail": "پسورد با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: "لینک بازیابی به ایمیل شما ارسال شد.", 400: "کاربری با این ایمیل پیدا نشد."},
        examples=[
            OpenApiExample(
                'مثال فراموشی پسورد',
                value={'email': 'user@example.com'},
                request_only=True,
            )
        ]
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            # اینجا باید عملیات ارسال ایمیل یا لینک بازیابی انجام شود
            return Response({"detail": "لینک بازیابی به ایمیل شما ارسال شد."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================= OTP CODE =============================

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({"error": "شماره تلفن الزامی است"}, status=400)

        code = str(random.randint(100000, 999999))
        OTP.objects.create(phone_number=phone_number, code=code)
        send_otp_sms(phone_number, code)

        return Response({"message": "کد ورود ارسال شد"})


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get("phone_number")
        code = request.data.get("code")

        try:
            otp = OTP.objects.filter(phone_number=phone_number, code=code).latest("created_at")
        except OTP.DoesNotExist:
            return Response({"error": "کد اشتباه است"}, status=400)

        if not otp.is_valid():
            return Response({"error": "کد منقضی شده است"}, status=400)

        user, created = User.objects.get_or_create(phone_number=phone_number)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        })
