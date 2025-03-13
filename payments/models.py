from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from extenstions.utils import jalali_converter
from reservations.models import Appointment

User = get_user_model()


class Wallet(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=" مبلغ مورد نظر (تومان)")

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول‌ها"

    def __str__(self):
        return f"کیف پول {self.user} با موجودی {self.balance}"

    def add_funds(self, amount):
        """افزودن مبلغ به موجودی کیف پول"""
        if amount > 0:
            self.balance += amount
            self.save()


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, blank=True, null=True,
                                    on_delete=models.CASCADE)  # اضافه کردن فیلد appointment
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"

    def __str__(self):
        return f"تراکنش {self.wallet.user} - {self.amount} تومان ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    def jcreated(self):
        return jalali_converter(self.created_at)


class UserWithdrawalRequests(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('paid', 'پرداخت شده'),
        ('canceled', 'رد شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='withdrawal_requests', verbose_name="کاربر")
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name='withdrawal_requests', verbose_name="نوبت")
    date = models.DateTimeField(verbose_name="تاریخ ثبت", auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")

    class Meta:
        verbose_name = "بدهی واریزی کاربران"
        verbose_name_plural = "بدهی واریز‌های کاربران"

    def __str__(self):
        return f"{self.user} - {self.appointment}"

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                previous = UserWithdrawalRequests.objects.get(pk=self.pk)
                if previous.status != self.status and self.status == 'paid':
                    wallet = Wallet.objects.get(user=self.user)
                    withdrawal_amount = self.appointment.service.price

                    if wallet.balance >= withdrawal_amount:
                        wallet.balance -= withdrawal_amount
                    else:
                        wallet.balance = 0  # یا پیام خطا مدیریت شود

                    wallet.save()
            except UserWithdrawalRequests.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def jcreated(self):
        return jalali_converter(self.date)
