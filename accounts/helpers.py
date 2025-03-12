import random
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def check_user_exist(new_phone):
    if User.objects.filter(phone_number=new_phone).exists():
        raise ValidationError([
            ValidationError(
                'این شماره موبایل قبلا ثبت شده است!', code='phone'),
        ])


def check_reset_password_sent(user):
    reset_password = user.password_resets.last()
    if reset_password:
        today = timezone.now()
        expiration = reset_password.created_at + timedelta(minutes=1)

        if today > expiration:
            return True

        return False

    return True
