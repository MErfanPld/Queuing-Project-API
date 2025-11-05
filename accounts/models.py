import random
import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings

class PasswordResetCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

    @staticmethod
    def generate_code(user):
        PasswordResetCode.objects.filter(user=user).delete()
        code = str(random.randint(10000, 99999))
        expires = timezone.now() + datetime.timedelta(minutes=5)
        return PasswordResetCode.objects.create(user=user, code=code, expires_at=expires)
