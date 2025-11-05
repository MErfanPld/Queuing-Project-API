# utils/sms.py
import requests

API_KEY = "456a6b916ca64f24bb14b5ca310a97bc"
BIRTHDAY_BODY_ID = 123456  # قالب تولد در ملی‌پیامک

def send_birthday_sms(phone_number, name):
    url = f"https://console.melipayamak.com/api/send/shared/{API_KEY}"
    payload = {
        "bodyId": BIRTHDAY_BODY_ID,
        "to": phone_number,
        "args": [name]
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print("خطا در ارسال پیامک:", e)
        return None