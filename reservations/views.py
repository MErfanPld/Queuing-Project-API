import json
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from acl.mixins import PermissionMixin
from business.models import Service
from .models import Appointment, AvailableTimeSlot
from payments.models import Wallet, Transaction, UserWithdrawalRequests
from .forms import AppointmentForm, GetAvailableTimesForm
from decimal import Decimal


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'reservations/reservation.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'pending'

        # بررسی موجود بودن زمان انتخابی
        selected_time = form.cleaned_data['time']
        selected_date = form.cleaned_data['date']
        service = form.cleaned_data['service']

        time_slot = AvailableTimeSlot.objects.filter(
            service=service, date=selected_date, time=selected_time, is_booked=False
        ).first()

        if not time_slot:
            form.add_error(
                'time', "این زمان دیگر در دسترس نیست، لطفا زمان دیگری انتخاب کنید.")
            return self.form_invalid(form)

        # علامت‌گذاری ساعت به‌عنوان رزرو شده
        time_slot.is_booked = True
        time_slot.save()

        response = super().form_valid(form)

        # ایجاد تراکنش و افزودن مبلغ به کیف پول کاربر
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        Transaction.objects.create(
            wallet=wallet, amount=service.price, appointment=form.instance)
        wallet.balance += Decimal(service.price)
        wallet.save()

        # ایجاد درخواست برداشت برای ادمین
        UserWithdrawalRequests.objects.create(
            user=self.request.user, appointment=form.instance)

        return redirect(reverse('payment', kwargs={'appointment_id': form.instance.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context


# ================================  Get Available Times ================================
def get_available_times(request):
    service_id = request.GET.get('service_id')
    date = request.GET.get('date')

    if not service_id or not date:
        return JsonResponse({'error': 'اطلاعات کامل ارسال نشده است'}, status=400)

    service = get_object_or_404(Service, id=service_id)
    available_times = AvailableTimeSlot.objects.filter(
        service=service, date=date, is_booked=False
    ).values_list('time', flat=True)

    return JsonResponse({'times': list(available_times)})

# ================================  Get Available Times CRUD ================================


class GetAvailableTimesListViewAdmin(PermissionMixin, ListView):
    permissions = ['get_available_list']
    model = AvailableTimeSlot
    context_object_name = 'get_available_list'
    template_name = 'reservations/get_available_times/get_available_admin_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context



class GetAvailableTimesCreateViewAdmin(PermissionMixin, CreateView):
    permissions = ['get_available_create']
    template_name = 'reservations/get_available_times/get_available_admin_form.html'
    model = AvailableTimeSlot
    form_class = GetAvailableTimesForm
    success_url = reverse_lazy("get-available-admin-list")


class GetAvailableTimesUpdateViewAdmin(PermissionMixin, UpdateView):
    permissions = ['get_available_edit']
    template_name = 'reservations/get_available_times/get_available_admin_form.html'
    model = AvailableTimeSlot
    form_class = GetAvailableTimesForm
    success_url = reverse_lazy("get-available-admin-list")


class GetAvailableTimesDeleteViewAdmin(PermissionMixin, DeleteView):
    permissions = ['get_available_delete']
    model = AvailableTimeSlot
    template_name = 'reservations/get_available_times/confirm_get_available_delete.html'
    success_url = reverse_lazy("get-available-admin-list")

# ================================  Update Appointment Status ================================


@require_POST
def update_appointment_status(request):
    appointment_id = request.POST.get('appointment_id')
    status = request.POST.get('status')
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = status
        appointment.save()
        return JsonResponse({'success': True, 'message': 'وضعیت به‌روزرسانی شد.'})
    except Appointment.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'رزرو یافت نشد.'})
