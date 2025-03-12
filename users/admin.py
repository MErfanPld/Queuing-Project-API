from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserModel = get_user_model()


class CustomUserAdmin(UserAdmin):
    ordering = ['phone']

    add_form = UserCreationForm
    form = UserChangeForm
    model = UserModel
    list_display = ['first_name', 'last_name', 'phone_number', 'is_superuser', 'is_active',
                    'is_staff']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )


admin.site.register(UserModel)
