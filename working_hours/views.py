from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from acl.mixins import PermissionMixin
from working_hours.filters import WorkingHoursFilters
from .models import WorkingHours
from .forms import WorkingHoursForm


class WorkingHoursListView(ListView):
    model = WorkingHours
    template_name = 'working_hours/work_hours.html'
    context_object_name = 'working_hours'


#? ============================= WorkingHours CRUD =============================
class WorkingHoursListViewAdmin(PermissionMixin, ListView):
    permissions = ['working_hours_list']
    model = WorkingHours
    context_object_name = 'WorkingHours_list'
    template_name = 'working_hours/work_hours_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return WorkingHoursFilters(data=self.request.GET, queryset=queryset).qs


class WorkingHoursCreateViewAdmin(PermissionMixin, CreateView):
    permissions = ['working_hours_create']
    template_name = 'working_hours/work_hours_form.html'
    model = WorkingHours
    form_class = WorkingHoursForm
    success_url = reverse_lazy("working-hours-list")


class WorkingHoursUpdateViewAdmin(PermissionMixin, UpdateView):
    permissions = ['working_hours_edit']
    template_name = 'working_hours/work_hours_form.html'
    model = WorkingHours
    form_class = WorkingHoursForm
    success_url = reverse_lazy("working-hours-list")


class WorkingHoursDeleteViewAdmin(PermissionMixin, DeleteView):
    permissions = ['working_hours_delete']
    model = WorkingHours
    template_name = 'working_hours/confirm_work_hours_delete.html'
    success_url = reverse_lazy("working-hours-list")
