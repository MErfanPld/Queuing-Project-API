from django.db.models.signals import post_save
from django.dispatch import receiver
from business.models import Business, Subscription
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=Business)
def create_trial_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(
            business=instance,
            trial_start=timezone.now(),
            trial_end=timezone.now() + timedelta(days=7),
            active=True
        )
