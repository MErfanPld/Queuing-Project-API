from django.db import models
from django.utils.text import slugify
import time


# Create your models here.


def upload_sliders_image(instance, filename):
    path = 'uploads/' + 'sliders/' + 'img' + \
        slugify(instance.title, allow_unicode=True)
    name = str(time.time()) + '-' + str(instance.title) + '-' + filename
    return path + '/' + name

class Slider(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    sub_title = models.CharField(max_length=255, verbose_name="متن")
    image = models.ImageField(upload_to=upload_sliders_image, verbose_name="تصویر", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "اسلایدر "
        verbose_name_plural = "اسلایدر ها"