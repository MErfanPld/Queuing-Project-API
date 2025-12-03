from django.db import models
from reservations.models import Appointment

class ReminderLog(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
