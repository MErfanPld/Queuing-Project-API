from django.db import models
from users.models import User
from business.models import AvailableTimeSlot, Service, Business
from extenstions.utils import jalali_converter
from business.models import Employee
from django.db import transaction
from payments.models import Transaction

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('confirmed', 'تایید شده'),
        ('canceled', 'لغو شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='appointments', verbose_name="کاربر")
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='appointments', verbose_name="سرویس")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True,
                                 null=True, related_name='appointments', verbose_name="کارمند")
    # date = models.DateField(verbose_name="تاریخ")
    # time = models.TimeField(verbose_name="زمان")
    time_slot = models.ForeignKey(AvailableTimeSlot, on_delete=models.CASCADE, related_name='appointments', verbose_name="بازه زمانی", null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='confirmed', verbose_name="وضعیت")
    reminder_sent = models.BooleanField(default=False, verbose_name="یادآوری ارسال شده")
    canceled_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان لغو")

    class Meta:
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"

    def __str__(self):
        return f"{self.user} - {self.service} - {self.status}"

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')

    def pay_with_wallet(self):
        from django.db import transaction
        from django.core.exceptions import ValidationError
        from payments.models import Transaction

        wallet = self.user.wallet  # فرض: کیف پول از قبل ایجاد شده

        from decimal import Decimal
        cost = self.service.price  # فرض: مدل Service فیلدی به نام price دارد

        if wallet.balance < cost:
            raise ValidationError("موجودی کیف پول کافی نیست.")

        with transaction.atomic():
            wallet = wallet.__class__.objects.select_for_update().get(pk=wallet.pk)

            if wallet.balance < cost:
                raise ValidationError("موجودی کیف پول کافی نیست.")

            wallet.decrease(cost)

            Transaction.objects.create(
                wallet=wallet,
                amount=cost,
                type='WITHDRAW',
                reservation=self,
                status='SUCCESS'
            )

            self.status = 'confirmed'
            self.save()

    def cancel(self, refund=True):
            """
            لغو رزرو + بازگشت وجه در صورت نیاز
            """
            from django.utils import timezone
            from payments.models import Transaction
            from django.core.exceptions import ValidationError

            if self.status == 'canceled':
                raise ValidationError("این رزرو قبلاً لغو شده است.")

            self.status = 'canceled'
            self.canceled_at = timezone.now()
            self.save()

            # اگر پرداخت با کیف پول بوده و refund True باشد
            if refund and hasattr(self.user, "wallet"):
                wallet = self.user.wallet
                cost = self.service.price

                wallet.increase(cost)

                Transaction.objects.create(
                    wallet=wallet,
                    amount=cost,
                    type='DEPOSIT',
                    reservation=self,
                    status='SUCCESS',
                    description='Refund after cancellation'
                )






    