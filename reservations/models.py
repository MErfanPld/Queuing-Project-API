from django.db import models
from users.models import User
from business.models import Service, Business
from extenstions.utils import jalali_converter
from business.models import Employee


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
    date = models.DateField(verbose_name="تاریخ")
    time = models.TimeField(verbose_name="زمان")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")

    class Meta:
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"

    def __str__(self):
        return f"{self.user} - {self.service} در {self.date} ساعت {self.time}"

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')


class AvailableTimeSlot(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="time_slots", verbose_name="سرویس")
    date = models.DateField(verbose_name="تاریخ")
    time = models.TimeField(verbose_name="ساعت در دسترس")
    is_booked = models.BooleanField(default=False, verbose_name="رزرو شده")

    class Meta:
        unique_together = ('service', 'date', 'time')
        verbose_name = "ساعت در دسترس"
        verbose_name_plural = "ساعت‌های در دسترس"

    def __str__(self):
        return f"{self.service.name} - {self.jdate()} {self.time.strftime('%H:%M')}"

    def jdate(self):
        return jalali_converter(self.date)

    # روش برای بررسی وضعیت رزرو
    @classmethod
    def check_available(cls, service, date, time):
        try:
            slot = cls.objects.get(service=service, date=date, time=time)
            return slot.is_booked == False
        except cls.DoesNotExist:
            return False