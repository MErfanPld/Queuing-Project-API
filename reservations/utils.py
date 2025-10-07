import requests

API_KEY = "e891feaac0144f48b8fbb68e72451d93"  # Access Key از پنل
PATTERN_CODE = "377065"                  # کد الگوی تایید شده
SENDER = "50002710046083"                # شماره خط خدماتی شما
SMS_URL = f"https://console.melipayamak.com/api/send/shared/{PATTERN_CODE}"


def send_reservation_sms(phone_number, name, date, time):
    """
    ارسال پیامک رزرو از طریق وب‌سرویس خدماتی ملی پیامک
    """
    payload = {
        "to": phone_number,
        "input_data": [
            {"0": name, "1": date, "2": time}  # مطابق شماره‌گذاری الگو
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"AccessKey {API_KEY}"
    }

    try:
        response = requests.post(SMS_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        print("✅ پیامک ارسال شد:", response.json())
        return response.json()
    except requests.RequestException as e:
        print("❌ خطا در ارسال پیامک:", e)
        if e.response is not None:
            print("📨 پاسخ سرور:", e.response.text)
        return None
