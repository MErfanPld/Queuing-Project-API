class CodeType:
    VERIFY = "verify"
    RESET_PASSWORD = "reset_password"
    CHOICES = (
        (VERIFY, "تایید حساب کاربری"),
        (RESET_PASSWORD, "بازیابی رمز عبور"),
    )
