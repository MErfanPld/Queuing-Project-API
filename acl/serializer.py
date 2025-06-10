from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from .models import *


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class Role_UserSerializer(ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
        depth = 1


class UserWithPermissionsSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name','last_name','permissions']

    def get_permissions(self, obj):
        user_permission = UserPermission.objects.filter(user=obj).first()
        if user_permission:
            return [{'id': perm.id, 'name': perm.name, 'code': perm.code} for perm in user_permission.permissions.all()]
        return []



class UserPermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True)

    permissions_display = serializers.SerializerMethodField()

    class Meta:
        model = UserPermission
        fields = ['user', 'id','permissions', 'permissions_display']

    def get_permissions_display(self, obj):
        return [perm.name for perm in obj.permissions.all()]

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', None)
        user = validated_data.get('user')

        if not User.objects.filter(id=user.id).exists():
            raise ValidationError("کاربر معتبر نیست.")

        user_permission = UserPermission.objects.create(**validated_data)
        if permissions_data is not None:
            user_permission.permissions.set(permissions_data)  # اصلاح شده
        return user_permission

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('permissions', None)

        if 'user' in validated_data:
            user = validated_data['user']
            if not User.objects.filter(id=user.id).exists():
                raise ValidationError("کاربر معتبر نیست.")
            instance.user = user

        instance.save()
        if permissions_data is not None:
            instance.permissions.set(permissions_data)  # اصلاح شده
        return instance