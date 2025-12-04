# reminders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from reservations.models import Appointment
from reminders.tasks import send_upcoming_appointment_reminders

@receiver(post_save, sender=Appointment)
def schedule_reminder(sender, instance, created, **kwargs):
    if created:
        # enqueue تسک برای این نوبت
        send_upcoming_appointment_reminders.delay(instance.id)
