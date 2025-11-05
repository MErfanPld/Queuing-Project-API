import requests

API_KEY = "456a6b916ca64f24bb14b5ca310a97bc"
BODY_ID = 386443 

def send_sms(phone, code):
    url = f"https://console.melipayamak.com/api/send/shared/{API_KEY}"
    payload = {
        "bodyId": BODY_ID,
        "to": phone,
        "args": [code]
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"SMS ارسال نشد: {response.text}")
    return response.json()
