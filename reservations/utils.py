import requests

API_KEY = "456a6b916ca64f24bb14b5ca310a97bc"  
BODY_ID = 382582                             

def send_reservation_sms(phone_number, name, date, time):
    url = f"https://console.melipayamak.com/api/send/shared/{API_KEY}"

    payload = {
        "bodyId": BODY_ID,
        "to": phone_number,
        "args": [name, date, time]
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            data = {"raw_response": response.text}

        print("✅ پیامک ارسال شد:", data)
        return data

    except requests.RequestException as e:
        print("❌ خطا در ارسال پیامک:", e)
        if hasattr(e, 'response') and e.response is not None:
            print("📨 پاسخ سرور:", e.response.text)
        return None


CANCEL_BODY_ID = 403828   

def send_cancel_sms(phone_number, name, service):
    """
    ارسال پیامک لغو نوبت با استفاده از قالب آماده ملی‌پیامک
    args = [name, service]
    """
    url = f"https://console.melipayamak.com/api/send/shared/{API_KEY}"

    payload = {
        "bodyId": CANCEL_BODY_ID,
        "to": phone_number,
        "args": [name, service]
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            data = {"raw_response": response.text}

        print("✅ پیامک لغو ارسال شد:", data)
        return data

    except requests.RequestException as e:
        print("❌ خطا در ارسال پیامک کنسلی:", e)
        if hasattr(e, 'response') and e.response is not None:
            print("📨 پاسخ سرور:", e.response.text)
        return None