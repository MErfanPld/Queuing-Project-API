from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and return a regular user with a phone number and password.
        """
        if not phone_number:
            raise ValueError('شماره تلفن الزامی است')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('سوپرکاربر باید is_superuser=True باشد')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('سوپرکاربر باید is_staff=True باشد')

        return self.create_user(phone_number, password, **extra_fields)
