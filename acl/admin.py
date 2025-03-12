from django.contrib import admin
from .models import *


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'description']
    # readonly_fields = ['created_at', 'updated_at']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'description']
    # readonly_fields = ['created_at', 'updated_at']


admin.site.register(UserRole)
admin.site.register(UserPermission)