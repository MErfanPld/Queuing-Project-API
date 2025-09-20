import requests

def send_otp_sms(phone_number, code):
    api_key = "API_KEY_تو_اینجا"
    url = "https://console.melipayamak.com/api/send/simple"
    payload = {
        "from": "شماره_خط_ارسالی",
        "to": phone_number,
        "text": f"کد ورود شما: {code}",
    }
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }
    requests.post(url, json=payload, headers=headers)
