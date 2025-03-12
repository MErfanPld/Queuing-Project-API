import json
import time
import requests
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf.urls.static import static
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from acl.permissions import PERMISSIONS
from extenstions.utils import jalali_converter
from utils.validator import mobile_regex, mobile_validator
from .managers import UserManager
from django.conf import settings
from django.utils.text import slugify


# Create your models here.


def upload_image(instance, filename):
    path = 'uploads/' + 'users/' + \
           slugify(instance.email, allow_unicode=True)
    name = str(time.time()) + '-' + str(instance.email) + '-' + filename
    return path + '/' + name


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    phone_number = models.CharField(
        max_length=11, unique=True, verbose_name="شماره تلفن")
    email = models.EmailField(('ایمیل'), null=True, blank=True, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ ویرایش")
    is_owner = models.BooleanField(('مالک هست؟'), default=False)
    is_superuser = models.BooleanField(('ادمین هست؟'), default=False)
    is_active = models.BooleanField(('فعال'), default=True)
    is_staff = models.BooleanField(('کارمند'), default=False)
    image = models.ImageField(
        ('تصویر'), upload_to='uploads/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.full_name

    def jcreated(self):
        return jalali_converter(self.created_at)

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = mobile_validator(
                str(self.phone_number)[:11]
            )

        if self.phone_number:
            qs = User.objects.filter(
                phone_number=self.phone_number
            )
            if self.pk:
                qs = qs.exclude(id=self.pk)
            if qs.exists():
                raise ValidationError(
                    'شماره موبایل تکراری است و برای کاربر دیگری استفاده شده است!',
                    code="mobile"
                )

        if self.email:
            qs = User.objects.filter(
                email=self.email
            )
            if self.pk:
                qs = qs.exclude(id=self.pk)
            if qs.exists():
                raise ValidationError(
                    'ایمیل تکراری است و برای کاربر دیگری استفاده شده است!',
                    code="email"
                )

        return super().save(*args, **kwargs)

    def get_phone(self):
        return self.phone_number

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email or '---'

    def user_role(self):
        return self.role if hasattr(self, 'role') else None

    @property
    def role_code(self):
        if hasattr(self, 'role') and self.role.role:
            return self.role.role.code
        else:
            return None

    @property
    def role_code_display(self):
        return self.role.role_name if hasattr(self, 'role') else 'کاربر'

    @property
    def has_role(self):
        if hasattr(self, 'role'):
            return True
        return False

    def change_role(self, role):
        from acl.models import UserRole
        user_role, _ = UserRole.objects.get_or_create(user=self)
        user_role.role = role
        user_role.save()
        return True

    @property
    def permissions(self):
        if self.is_superuser:
            return PERMISSIONS
        else:
            try:
                return self.user_permission.permissions_list
            except:
                return []

    def check_has_permission(self, permission):
        if permission in self.permissions:
            return True
        return False

    def get_avatar(self):
        return self.image.url if self.image else 'static/img/user-3.jpg'
