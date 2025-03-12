from django.db import models
# from utils.models import CustomModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام نمایشی')
    code = models.CharField(verbose_name='عنوان انگلیسی', max_length=255, unique=True)
    description = models.TextField(max_length=500, verbose_name='توضیحات', null=True, blank=True)
    permissions = models.ManyToManyField(to='Permission', related_name='role', verbose_name='نقش ها', blank=True)

    class Meta:
        verbose_name = 'نقش'
        verbose_name_plural = 'نقش ها'

    def __str__(self):
        return f"{self.name}"

    @property
    def permissions_list(self):
        return list(self.permissions.values_list('code', flat=True))


class Permission(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام نمایشی')
    code = models.CharField(verbose_name='عنوان انگلیسی', max_length=255, unique=True)
    description = models.TextField(max_length=500, verbose_name='توضیحات', null=True, blank=True)

    class Meta:
        verbose_name = 'دسترسی'
        verbose_name_plural = 'دسترسی ها'

    def __str__(self):
        return f"{self.name}-{self.code}"


class UserRole(models.Model):
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, related_name='users', verbose_name='نقش', null=True,
                             blank=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='role', verbose_name='کاربر')

    class Meta:
        verbose_name = 'نقش کاربر'
        verbose_name_plural = 'نقش کاربران'

    def __str__(self):
        return f"{self.user}-{self.role.name}"

    @property
    def role_name(self):
        if self.role:
            return self.role.name
        return 'کاربر'


class UserPermission(models.Model):
    permissions = models.ManyToManyField(to=Permission, related_name='users',
                                         verbose_name='دسترسی ها', blank=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user_permission', verbose_name='کاربر')

    class Meta:
        verbose_name = 'دسترسی کاربر'
        verbose_name_plural = 'دسترسی کاربران'

    def __str__(self):
        return f"{self.user}"

    @property
    def permissions_name(self):
        return [item.name for item in self.permissions.all()]

    @property
    def permissions_list(self):
        return list(self.permissions.values_list('code', flat=True))
