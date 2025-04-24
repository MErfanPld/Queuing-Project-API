from django.db import models


class WorkingHours(models.Model):
    day = models.DateField(unique=True,verbose_name="روز")
    opening_time = models.TimeField(verbose_name="ساعت شروع")
    closing_time = models.TimeField(verbose_name="ساعت پایان")

    def __str__(self):
        return f"{self.day} - {self.opening_time.strftime('%H:%M')} to {self.closing_time.strftime('%H:%M')}"
