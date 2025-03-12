from django.core.validators import RegexValidator
import re
from unidecode import unidecode
from django.forms import forms

national_id_regex = RegexValidator(
    regex=r"^\d{10}$",
    message="شناسه ملی معتبر نیست."
)

mobile_regex = RegexValidator(
    regex=r'(^\+?(09|98|0)?(9([0-9]{9}))$)',
    message="شماره موبایل معتبر نیست."
)

mobile_pattern = r'^\+?(09|98|0)?(9([0-9]{9}))$'


def mobile_validator(mobile):
    if not mobile:
        return ''

    m = re.search(mobile_pattern, mobile)
    if not m:
        return ''
    mobile = '0' + str(m.group(2))
    mobile = unidecode(mobile)  # Convert to english always!
    return mobile


def validate_file_size(value):
    filesize = value.size

    if filesize > 5000 * 1024:
        raise forms.ValidationError("حداکثر حجم قابل آپلود 5 کیلوبایت است.")
    else:
        return value
