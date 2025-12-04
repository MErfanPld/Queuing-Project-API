import requests
from django.utils import timezone
from extenstions.utils import jalali_converter

API_KEY = "456a6b916ca64f24bb14b5ca310a97bc"
REMINDER_BODY_ID = 401682  


def send_reminder_sms(phone, name, time):
    """
    ارسال پیامک یادآوری نوبت با متن فارسی و تاریخ شمسی
    """
    # تبدیل تاریخ و ساعت به شمسی
    date_str = jalali_converter(time.date())  # فقط تاریخ
    time_str = f"{time.hour}:{time.minute}" 

    payload = {
        "bodyId": REMINDER_BODY_ID,
        "to": phone,
        "args": [
            name,       # {0} نام کاربر
            date_str,   # {1} تاریخ شمسی
            time_str    # {2} ساعت
        ]
    }

    url = f"https://console.melipayamak.com/api/send/shared/{API_KEY}"

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





# def send_reminder_sms(phone, name, date, time):
#     """
#     ارسال پیامک یادآور نوبت با ملی‌پیامک
#     """
#     url = f"https://console.melipayamak.com/api/send/shared/{API_KEY}"

#     payload = {
#         "bodyId": REMINDER_BODY_ID,
#         "to": phone,
#         "args": [name, date, time]
#     }

#     try:
#         response = requests.post(url, json=payload, timeout=10)
#         response.raise_for_status()

#         try:
#             data = response.json()
#         except ValueError:
#             data = {"raw_response": response.text}

#         print("✔ پیامک یادآوری ارسال شد:", data)
#         return True

#     except requests.RequestException as e:
#         print("❌ خطا در ارسال یادآوری:", e)
#         return False
