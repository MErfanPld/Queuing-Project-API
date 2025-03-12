from django import template
import jdatetime
import datetime

from extenstions.utils import jalali_converter

register = template.Library()


@register.filter(name='jalali_date')
def jalali_date_filter(date):
    if isinstance(date, (datetime.date, datetime.datetime)):
        return jdatetime.date.fromgregorian(date=date).strftime('%Y/%m/%d')
    return ''


@register.filter(name='jalali_time')
def jalali_time_filter(time):
    if isinstance(time, (datetime.time, datetime.datetime)):
        return time.strftime('%H:%M')
    return ''


@register.filter(name='jalali_converter_date')
def jalali_converter_date_filter(value):
    return jalali_converter(value)
