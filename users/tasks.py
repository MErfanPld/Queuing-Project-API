# users/tasks.py
from celery import shared_task
from django.utils import timezone
from users.models import User
from .sms import send_birthday_sms

@shared_task
def send_daily_birthday_sms():
    today = timezone.localdate()
    users = User.objects.filter(
        birthday_day=today.day,
        birthday_month=today.month,
        is_active=True,
        birthday_day__isnull=False,
        birthday_month__isnull=False
    )

    sent_count = 0
    for user in users:
        name = user.first_name.strip() if user.first_name else "عزیز"
        result = send_birthday_sms(user.phone_number, name)
        if result and result.get('StrRetStatus') == 'Ok':
            sent_count += 1

    print(f"تعداد پیامک‌های تولد ارسال‌شده: {sent_count}")
    return sent_count