from django import forms
from .models import *


class RoleForm(forms.ModelForm):
    permissions = forms.CharField(required=False, label='دسترسی‌ها')

    class Meta:
        model = Role
        fields = '__all__'

    def clean_permissions(self):
        if self.cleaned_data.get('permissions'):
            permissions = self.cleaned_data.get('permissions').split(',')
        else:
            permissions = []

        if len(permissions) == 0:
            raise forms.ValidationError('حداقل یک دسترسی باید در نقش وجود داشته باشد.')

        return permissions


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance:
            self.fields['user'].queryset = User.objects.filter(role__isnull=True)


class UserPermissionForm(forms.ModelForm):
    permissions = forms.CharField(required=False, label='دسترسی‌ها')

    class Meta:
        model = UserPermission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.id:
            self.fields['user'].queryset = User.objects.filter(user_permission__isnull=True)

    def clean_permissions(self):
        print('ffffffffffffffff')
        print(self.cleaned_data.get('permissions'))

        if self.cleaned_data.get('permissions'):
            permissions = self.cleaned_data.get('permissions').split(',')
        else:
            permissions = []

        if len(permissions) == 0:
            raise forms.ValidationError('حداقل یک دسترسی باید در نقش وجود داشته باشد.')

        return permissions
