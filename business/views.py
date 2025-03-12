from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from payments.models import Wallet, Transaction
from acl.mixins import PermissionMixin
from reservations.models import Appointment
from .models import Business, Employee, Service
from .forms import BusinessForm, EmployeeForm, ServiceForm
from .filters import EmployeeFilters, ServiceFilters

# Create your views here.

#? ============================= Paid Services =============================
class PaidServicesView(ListView):
    template_name = 'business/admin/paid_services.html'
    context_object_name = 'service_data'
    
    def get_queryset(self):
        # گرفتن تمام تراکنش‌های مرتبط با اپوینتمنت‌ها
        transactions = Transaction.objects.values_list('appointment_id', flat=True)
        # گرفتن اپوینتمنت‌های مرتبط با این تراکنش‌ها
        appointments_with_transactions = Appointment.objects.filter(id__in=transactions)
        # گرفتن خدمات مرتبط با این اپوینتمنت‌ها
        services_with_payments = Service.objects.filter(appointments__in=appointments_with_transactions).distinct()
        return services_with_payments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_data = []

        for service in self.get_queryset():
            # جمع‌آوری نام مالک برای هر سرویس
            owner_name = service.business.name if service.business else 'نامشخص'
            service_data.append({
                'service': service,
                'owner_name': owner_name
            })

        context['service_data'] = service_data
        return context

#? ============================= Services CRUD =============================
class ServiceListView(PermissionMixin, ListView):
    permissions = ['service_list']
    model = Service
    context_object_name = 'service_list'
    template_name = 'business/admin/services/service_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return ServiceFilters(data=self.request.GET, queryset=queryset).qs


class ServiceCreateView(PermissionMixin, CreateView):
    permissions = ['service_create']
    template_name = "business/admin/services/service_form.html"
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy("service-list")


class ServiceUpdateView(PermissionMixin, UpdateView):
    permissions = ['service_edit']
    template_name = "business/admin/services/service_form.html"
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy("service-list")


class ServiceDeleteView(PermissionMixin, DeleteView):
    permissions = ['service_delete']
    model = Service
    template_name = 'business/admin/services/confirm_service_delete.html'
    success_url = reverse_lazy("service-list")


#? ============================= Employee CRUD =============================
class EmployeeListView(PermissionMixin, ListView):
    permissions = ['employee_list']
    model = Employee
    context_object_name = 'employee_list'
    template_name = 'business/admin/employee/employee_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return EmployeeFilters(data=self.request.GET, queryset=queryset).qs


class EmployeeCreateView(PermissionMixin, CreateView):
    permissions = ['employee_create']
    template_name = "business/admin/employee/employee_form.html"
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("employee-list")


class EmployeeUpdateView(PermissionMixin, UpdateView):
    permissions = ['employee_edit']
    template_name = "business/admin/employee/employee_form.html"
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("employee-list")


class EmployeeDeleteView(PermissionMixin, DeleteView):
    permissions = ['employee_delete']
    model = Employee
    template_name = 'business/admin/employee/confirm_employee_delete.html'
    success_url = reverse_lazy("employee-list")

#? ============================= Business CRUD =============================
class BusinessListView(PermissionMixin, ListView):
    permissions = ['business_list']
    model = Business
    context_object_name = 'business_list'
    template_name = 'business/admin/business/business_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class BusinessCreateView(PermissionMixin, CreateView):
    permissions = ['business_create']
    template_name = "business/admin/business/business_form.html"
    model = Business
    form_class = BusinessForm
    success_url = reverse_lazy("business-list")


class BusinessUpdateView(PermissionMixin, UpdateView):
    permissions = ['business_edit']
    template_name = "business/admin/business/business_form.html"
    model = Business
    form_class = BusinessForm
    success_url = reverse_lazy("business-list")


class BusinessDeleteView(PermissionMixin, DeleteView):
    permissions = ['business_delete']
    model = Business
    template_name = 'business/admin/business/confirm_business_delete.html'
    success_url = reverse_lazy("business-list")
