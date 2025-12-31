from django.db import models
 
class Feature(models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=100)
    key = models.SlugField(verbose_name='کلید',unique=True) 
    description = models.TextField(verbose_name='توضیحات',blank=True)

    def __str__(self):
        return self.title


class Plan(models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=100)
    price = models.PositiveIntegerField(verbose_name='قیمت')
    duration_days = models.PositiveIntegerField(verbose_name='زمان')
    is_active = models.BooleanField(verbose_name='فعال؟',default=True)

    def __str__(self):
        return self.title


class PlanFeature(models.Model):
    plan = models.ForeignKey(
        Plan,
        verbose_name='پلن',
        on_delete=models.CASCADE,
        related_name='features'
    )
    feature = models.ForeignKey(
        Feature,
        verbose_name='ویژگی',
        on_delete=models.CASCADE
    )

    value = models.CharField(
        max_length=100,
        help_text="مثلا: دارد / ندارد / 5 / نامحدود"
    )

    class Meta:
        unique_together = ('plan', 'feature')
