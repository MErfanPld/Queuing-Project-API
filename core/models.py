from django.db import models

# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    sub_title = models.CharField(max_length=255, verbose_name="متن")
    is_active = models.BooleanField(default=True, verbose_name="فعال؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "اسلایدر "
        verbose_name_plural = "اسلایدر ها"