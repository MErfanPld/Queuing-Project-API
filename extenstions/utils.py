from . import jalali
from django.utils import timezone
from datetime import date, datetime

def persion_numbers_converter(mystr):
    """تبدیل اعداد به فارسی"""
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }
    for e, p in numbers.items():
        mystr = mystr.replace(e, p)
    return mystr

def jalali_converter(time):
    """تبدیل تاریخ میلادی به شمسی"""
    jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    
    # بررسی نوع ورودی
    if isinstance(time, datetime):
        time = timezone.localtime(time)
    elif isinstance(time, date):
        time = time

    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    # تبدیل ماه به نام ماه شمسی
    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    # بررسی و افزودن زمان به خروجی اگر ورودی از نوع datetime بود
    if isinstance(time, datetime):
        output = "{} {} {}، ساعت {}:{}".format(
            time_to_list[2],
            time_to_list[1],
            time_to_list[0],
            time.hour,
            time.minute
        )
    else:
        output = "{} {} {}".format(
            time_to_list[2],
            time_to_list[1],
            time_to_list[0]
        )
    
    return persion_numbers_converter(output) 
