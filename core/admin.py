from django.contrib import admin
from .models import Slider

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")  # نمایش این فیلدها در لیست
    list_filter = ("is_active",)  # امکان فیلتر کردن بر اساس وضعیت فعال/غیرفعال
    search_fields = ("title",)  # جستجو بر اساس عنوان
    ordering = ("-created_at",)  # مرتب‌سازی بر اساس تاریخ ایجاد (جدیدترین‌ها بالا)

admin.site.site_header = "مدیریت نوبت دهی"
admin.site.site_title = "پنل مدیریت نوبت دهی"
admin.site.index_title = "به پنل مدیریت خوش آمدید"
