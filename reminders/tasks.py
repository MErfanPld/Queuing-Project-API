from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from reservations.models import Appointment
from reminders.utils import send_reminder_sms


@shared_task
def send_upcoming_appointment_reminders():
    """
    بررسی همه نوبت‌های تایید شده و ارسال پیامک یادآوری
    یک ساعت قبل از زمان نوبت برای همه کاربران
    """
    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)

    # فیلتر همه نوبت‌های تایید شده و بدون یادآوری
    appointments = Appointment.objects.filter(
        status='confirmed',
        reminder_sent=False,
        time_slot__date__gte=now.date(),  # تاریخ امروز یا بعد
    )

    for ap in appointments:
        # ترکیب date و start_time برای بررسی دقیق
        ap_datetime = timezone.make_aware(
            timezone.datetime.combine(ap.time_slot.date, ap.time_slot.start_time)
        )

        # بررسی اینکه زمان نوبت در بازه یک ساعت آینده است
        if now <= ap_datetime <= one_hour_later:
            user = ap.user

            # نام و شماره واقعی کاربر
            name = getattr(user, "fullname", getattr(user, "name", "کاربر"))
            phone = getattr(user, "phone", getattr(user, "mobile", None))

            if not phone:
                print(f"❌ کاربر {user.id} شماره موبایل ندارد، یادآوری ارسال نشد.")
                continue

            date_str = ap.time_slot.date.strftime("%Y-%m-%d")
            time_str = ap.time_slot.start_time.strftime("%H:%M")

            # ارسال پیامک
            sent = send_reminder_sms(
                phone=phone,
                name=name,
                date=date_str,
                time=time_str
            )

            if sent:
                ap.reminder_sent = True
                ap.save()
                print(f"✔ یادآوری برای Appointment {ap.id} ارسال شد.")
            else:
                print(f"❌ ارسال پیامک برای Appointment {ap.id} ناموفق بود.")
