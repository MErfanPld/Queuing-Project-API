from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserAdmin(BaseUserAdmin):
    # نمایش فیلدها در لیست ادمین
    list_display = ('phone_number', 'first_name', 'last_name', 'is_owner', 'is_superuser', 'is_active', 'is_staff')

    # فیلتر کردن بر اساس وضعیت‌های خاص
    list_filter = ('is_superuser', 'is_active', 'is_staff', 'is_owner')

    # بخش‌های مختلف فرم در ادمین
    fieldsets = (
        ("اطلاعات اصلی", {'fields': ('phone_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'image')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_owner', 'groups', 'user_permissions')}),
        # حذف فیلد تاریخ ویرایش
    )

    # فیلدهای اضافه برای فرم ثبت‌نام
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_owner')}),
    )

    # قابلیت جستجو بر اساس فیلدها
    search_fields = ['phone_number', 'first_name', 'last_name']
    # ترتیب نمایش در ادمین
    ordering = ('phone_number',)
    # فیلدهای انتخابی افقی
    filter_horizontal = ()

admin.site.register(UserModel, UserAdmin)
