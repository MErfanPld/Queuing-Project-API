from melipayamak import Api

def send_sms(phone_number, message):
    try:
        username = "9912146083"  # نام کاربری پنل ملی پیامک
        password = "g75c2"  # رمز عبور پنل ملی پیامک
        api = Api(username, password)
        sms = api.sms()
        sender = "50002710046083"  # شماره خط اختصاصی
        sms.send(phone_number, sender, message)
    except Exception as e:
        print("SMS Error:", e)
