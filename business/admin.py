from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Business)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(AvailableTimeSlot)
