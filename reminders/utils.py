import requests
from django.utils import timezone

API_KEY = "456a6b916ca64f24bb14b5ca310a97bc"
REMINDER_BODY_ID = 389200   # همان BodyID الگوی یادآوری

def send_reminder_sms(phone, name, date, time):
    """
    ارسال پیامک یادآور نوبت با ملی‌پیامک
    """
    url = f"https://console.melipayamak.com/api/send/shared/{API_KEY}"

    payload = {
        "bodyId": REMINDER_BODY_ID,
        "to": phone,
        "args": [name, date, time]
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            data = {"raw_response": response.text}

        print("✔ پیامک یادآوری ارسال شد:", data)
        return True

    except requests.RequestException as e:
        print("❌ خطا در ارسال یادآوری:", e)
        return False
