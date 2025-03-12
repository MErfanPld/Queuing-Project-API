from django.conf import settings
from django.db import models
from decimal import Decimal
from business.models import Service, Business


class Package(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='packages', verbose_name="کسب‌وکار")
    name = models.CharField(max_length=255, verbose_name="نام پکیج")
    services = models.ManyToManyField(
        Service, related_name="packages", verbose_name="سرویس‌ها")
    desc = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="قیمت کل")
    image = models.ImageField(verbose_name="تصویر", null=True, blank=True)
    media_files = models.FileField(
        default=list, blank=True, verbose_name="تصاویر و ویدیوها")

    class Meta:
        verbose_name = "پکیج"
        verbose_name_plural = "پکیج‌ها"

    def __str__(self):
        return self.name

    def calculate_total_price(self):
        """محاسبه قیمت کل پکیج بر اساس سرویس‌های انتخاب شده"""
        total = sum(service.price for service in self.services.all())
        return Decimal(total)

    def save(self, *args, **kwargs):
        """ابتدا شیء را ذخیره کرده و سپس مقدار `total_price` را محاسبه و ذخیره می‌کنیم"""
        super().save(*args, **kwargs)
        self.total_price = self.calculate_total_price()
        super().save(update_fields=['total_price'])

    def average_rating(self):
        """محاسبه میانگین امتیاز نظرات این پکیج"""
        return self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0


class PackageReview(models.Model):
    package = models.ForeignKey(
        'Package', on_delete=models.CASCADE, related_name='reviews', verbose_name="پکیج")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='package_reviews', verbose_name="کاربر")
    rating = models.PositiveSmallIntegerField(verbose_name="امتیاز", default=1)
    comment = models.TextField(verbose_name="نظر", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "نظر پکیج"
        verbose_name_plural = "نظرات پکیج"
        unique_together = ('package', 'user')

    def __str__(self):
        return f"{self.user} - {self.package} ({self.rating} ستاره)"
