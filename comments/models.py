from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Comment(models.Model):
    TARGET_CHOICES = (
        ('service', 'سرویس'),
        ('business', 'کسب‌وکار'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    target_type = models.CharField(max_length=10, choices=TARGET_CHOICES)
    service = models.ForeignKey(
        'business.Service', on_delete=models.CASCADE, null=True, blank=True, related_name='comments'
    )
    business = models.ForeignKey(
        'business.Business', on_delete=models.CASCADE, null=True, blank=True, related_name='comments'
    )
    content = models.TextField(verbose_name='متن نظر')
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='امتیاز (۱ تا ۵)')
    is_approved = models.BooleanField(default=False, verbose_name='تأیید شده')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'نظر کاربر'
        verbose_name_plural = 'نظرات کاربران'

    def __str__(self):
        target_name = (
            self.service.name if self.target_type == 'service' and self.service else
            self.business.name if self.business else '---'
        )
        return f"{self.user} درباره {self.get_target_type_display()} {target_name}"

    def clean(self):
        if self.target_type == 'service' and not self.service:
            raise ValueError("برای نوع 'service' باید فیلد service مشخص شود.")
        if self.target_type == 'business' and not self.business:
            raise ValueError("برای نوع 'business' باید فیلد business مشخص شود.")
