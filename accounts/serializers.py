from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


from drf_spectacular.utils import OpenApiExample

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, help_text="پسورد فعلی")
    new_password = serializers.CharField(required=True, help_text="پسورد جدید")
    confirm_password = serializers.CharField(required=True, help_text="تایید پسورد جدید")

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("پسورد جدید و تایید پسورد باید یکی باشند.")
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="ایمیل کاربر")