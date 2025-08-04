import datetime
from django.db import models
from users.models import User
from datetime import datetime


# Create your models here.


class Business(models.Model):
    BUSINESS_TYPES = [
        ('آرایشگاه', 'آرایشگاه'),
        ('مراکز پوست', 'مراکز پوست'),
        # ('restaurant', 'رستوران'),
        # ('clinic', 'مطب'),
        # ('immigration_office', 'دفتر مهاجرت'),
    ]

    name = models.CharField(max_length=255, verbose_name="نام کسب‌وکار")
    business_type = models.CharField(
        max_length=20, choices=BUSINESS_TYPES, verbose_name="نوع کسب‌وکار")
    address = models.CharField(max_length=255, verbose_name="آدرس")
    telephone_number = models.CharField(
        max_length=15, verbose_name="شماره تلفن")
    phone_number = models.CharField(max_length=15, verbose_name="شماره همراه")
    is_coffee_shop = models.BooleanField(
        default=False, verbose_name="کافی شاپ دارد؟")
    is_parking = models.BooleanField(
        default=False, verbose_name="پارکینگ دارد؟")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="صاحب کسب‌وکار")
    instagram_link = models.URLField(
        max_length=200, verbose_name="لینک اینستاگرام")

    class Meta:
        verbose_name = "کسب‌وکار"
        verbose_name_plural = "کسب‌وکارها"

    def __str__(self):
        return f"{self.name} ({self.get_business_type_display()})"


class Employee(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=" کارمند")
    skill = models.CharField(max_length=255, verbose_name="نام مهارت")

    class Meta:
        verbose_name = "کارمند"
        verbose_name_plural = "کارمندان"

    def __str__(self):
        return f"{self.user} ({self.skill})"


class Service(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='services', verbose_name="کسب‌وکار")
    name = models.CharField(max_length=255, verbose_name="نام سرویس")
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, blank=True, null=True, related_name='services', verbose_name="کارمند")
    description = models.TextField(verbose_name="توضیحات")
    duration = models.DurationField(
        help_text="مدت زمان به صورت HH:MM:SS", verbose_name="مدت زمان تقریبی")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="قیمت بیانه")

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس‌ها"

    def __str__(self):
        return f"{self.name} | {self.employee} ({self.business.name})"

    def get_price(self):
        return self.price



class AvailableTimeSlot(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='available_slots')
    date = models.DateField(verbose_name="تاریخ")
    start_time = models.TimeField(verbose_name="ساعت شروع")
    is_available = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    class Meta:
        unique_together = ('service', 'date', 'start_time')
        verbose_name = "ساعت دردسترس"
        verbose_name_plural = "ساعت های دردسترس"
        
    @property
    def end_time(self):
        start_dt = datetime.combine(self.date, self.start_time)
        return (start_dt + self.service.duration).time()
    