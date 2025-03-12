# from django.conf import settings
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from acl.filters import PermissionFilters, RoleFilters, UserRoleFilters, UserPermissionFilters
from acl.forms import RoleForm, PermissionForm, UserRoleForm, UserPermissionForm
from acl.models import *
from django.contrib.auth import get_user_model

from acl.permissions import PERMISSIONS, filter_permissions
from acl.mixins import SuperUserRequiredMixin, PermissionMixin

User = get_user_model()


class RolesListView(SuperUserRequiredMixin, ListView):
    model = Role
    context_object_name = 'roles'
    # paginate_by = settings.PAGINATION_NUMBER
    # ordering = ['-updated_at']
    template_name = 'acl/admin/roles/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return RoleFilters(data=self.request.GET, queryset=queryset).qs


class RolesCreateView(SuperUserRequiredMixin, CreateView):
    model = Role
    template_name = 'acl/admin/roles/form.html'
    form_class = RoleForm
    success_url = reverse_lazy('roles-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['permissions'] = PERMISSIONS
        return context


class RolesUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'acl/admin/roles/form.html'
    success_url = reverse_lazy('roles-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['permissions'] = PERMISSIONS
        return context


class RolesDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Role
    template_name = 'acl/admin/roles/list.html'
    success_url = reverse_lazy('roles-list')

    def dispatch(self, *args, **kwargs):
        resp = super().dispatch(*args, **kwargs)
        messages.success(self.request, 'نقش مورد نظر با موفقیت حدف شد.')
        return resp


############################################################################

class RoleUserListView(SuperUserRequiredMixin, ListView):
    model = UserRole
    context_object_name = 'user_roles'
    # paginate_by = settings.PAGINATION_NUMBER
    ordering = ['-updated_at']
    template_name = 'acl/admin/user_roles/list.html'
    queryset = UserRole.objects.filter(role__isnull=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        return UserRoleFilters(data=self.request.GET, queryset=queryset).qs


class RoleUserCreateView(SuperUserRequiredMixin, CreateView):
    template_name = "acl/admin/user_roles/form.html"
    model = UserRole
    form_class = UserRoleForm
    success_url = reverse_lazy('role-user-list')

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('user'):
            try:
                User.objects.get(pk=self.request.GET.get('user'))
            except:
                raise Http404

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return self.success_url


class RoleUserUpdateView(SuperUserRequiredMixin, UpdateView):
    model = UserRole
    form_class = UserRoleForm
    template_name = "acl/admin/user_roles/form.html"
    success_url = reverse_lazy('role-user-list')

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('user'):
            try:
                User.objects.get(pk=self.request.GET.get('user'))
            except:
                raise Http404

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return self.success_url


class RoleUserDeleteView(SuperUserRequiredMixin, DeleteView):
    model = UserRole
    template_name = 'acl/admin/user_roles/list.html'
    success_url = reverse_lazy('role-user-list')

    def dispatch(self, *args, **kwargs):
        resp = super().dispatch(*args, **kwargs)
        messages.success(self.request, 'کاربر مدیر مورد نظر با موفقیت حدف شد.')
        return resp


############################################################################


class UserPermissionsListView(PermissionMixin, ListView):
    permissions = ['user_permissions_list']
    model = UserPermission
    # paginate_by = settings.PAGINATION_NUMBER
    # ordering = ['-updated_at']
    template_name = 'acl/admin/user_permissions/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return UserPermissionFilters(data=self.request.GET, queryset=queryset).qs


class UserPermissionsCreateView(PermissionMixin, CreateView):
    permissions = ['user_permissions_create']
    model = UserPermission
    template_name = 'acl/admin/user_permissions/form.html'
    form_class = UserPermissionForm
    success_url = reverse_lazy('permission-user-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        if self.request.user.is_staff:
            context['permissions'] = PERMISSIONS
        else:
            user_permissions = self.request.user.permissions
            context['permissions'] = filter_permissions(PERMISSIONS, user_permissions)

        return context


class UserPermissionsUpdateView(PermissionMixin, UpdateView):
    permissions = ['user_permissions_edit']
    model = UserPermission
    form_class = UserPermissionForm
    template_name = 'acl/admin/user_permissions/form.html'
    success_url = reverse_lazy('permission-user-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        if self.request.user.is_staff:
            context['permissions'] = PERMISSIONS
        else:
            user_permissions = self.request.user.permissions
            context['permissions'] = filter_permissions(PERMISSIONS, user_permissions)

        return context


class UserPermissionsDeleteView(PermissionMixin, DeleteView):
    permissions = ['user_permissions_delete']
    model = UserPermission
    template_name = 'acl/admin/user_permissions/confirm_delete.html'
    success_url = reverse_lazy('permission-user-list')

    def dispatch(self, *args, **kwargs):
        resp = super().dispatch(*args, **kwargs)
        messages.success(self.request, 'آیتم مورد نظر با موفقیت حدف شد.')
        return resp
