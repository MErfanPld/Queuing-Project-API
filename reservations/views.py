from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from datetime import datetime

from acl.rest_mixin import RestPermissionMixin
from reservations.models import Appointment
from business.models import AvailableTimeSlot
from reservations.serializers import AppointmentSerializer
from reservations.utils import send_cancel_sms, send_reservation_sms


# ============================== Appointment CRUD ==============================
class AppointmentListCreateView(generics.ListCreateAPIView):
    """نوبت‌های خود مشتری"""
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

    @transaction.atomic
    def perform_create(self, serializer):
        appointment = serializer.save(user=self.request.user, status='confirmed')
        
        slot = appointment.time_slot
        slot.is_available = False
        slot.save(update_fields=['is_available'])

        phone = appointment.user.phone_number
        name = appointment.user.first_name or "کاربر"
        date = str(appointment.time_slot.date)
        time_ = str(appointment.time_slot.start_time)
        send_reservation_sms(phone, name, date, time_)


class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """جزئیات و حذف نوبت مشتری"""
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)


# ============================== Appointment Cancel ==============================
class AppointmentCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)

        # دسترسی: فقط خود کاربر یا superuser
        if not request.user.is_superuser and appointment.user != request.user:
            return Response({"error": "دسترسی ندارید"}, status=403)

        # لغو نوبت + بازگشت وجه
        appointment.cancel(refund=True)

        # باز کردن time_slot برای رزرو بعدی
        slot = appointment.time_slot
        slot.is_available = True
        slot.save(update_fields=['is_available'])

        # ارسال پیامک لغو
        send_cancel_sms(
            appointment.user.phone_number,
            appointment.user.first_name or "کاربر",
            appointment.service.name
        )

        return Response({"message": "نوبت با موفقیت لغو شد."}, status=200)




from reservations.serializers import AppointmentSerializer, AppointmentBusinessSerializer


# ============================== برای صاحب ارایشگاه ==============================
class BusinessAppointmentListView(generics.ListAPIView):
    """
    لیست نوبت‌های ارایشگاه برای صاحب کسب‌وکار
    """
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['reservations_list']
    serializer_class = AppointmentBusinessSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        
        # فقط نوبت‌های ارایشگاه‌های متعلق به کاربر
        return Appointment.objects.filter(
            time_slot__service__business__owner=user
        ).select_related(
            'user', 'service', 'employee', 'time_slot'
        ).order_by('-time_slot__date', '-time_slot__start_time')

    def get(self, request, *args, **kwargs):
        # فیلتر اختیاری با query parameters
        queryset = self.get_queryset()
        
        status = request.query_params.get('status')
        date = request.query_params.get('date')
        service_id = request.query_params.get('service_id')

        if status:
            queryset = queryset.filter(status=status)
        if date:
            queryset = queryset.filter(time_slot__date=date)
        if service_id:
            queryset = queryset.filter(service_id=service_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BusinessAppointmentUpdateView(generics.UpdateAPIView):
    """
    تایید/رد نوبت توسط صاحب ارایشگاه
    """
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['reservations_edit']
    serializer_class = AppointmentBusinessSerializer

    def get_queryset(self):
        return Appointment.objects.filter(
            time_slot__service__business__owner=self.request.user
        )

    def update(self, request, *args, **kwargs):
        appointment = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['pending', 'confirmed', 'canceled']:
            return Response({"error": "وضعیت نامعتبر است"}, status=400)

        old_status = appointment.status
        appointment.status = new_status
        appointment.save()

        # اگر لغو شد، اسلات آزاد بشه
        if new_status == 'canceled' and old_status != 'canceled':
            slot = appointment.time_slot
            slot.is_available = True
            slot.save(update_fields=['is_available'])

            # ارسال پیامک لغو به مشتری
            send_cancel_sms(
                appointment.user.phone_number,
                appointment.user.first_name or "کاربر",
                appointment.service.name
            )

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class BusinessAppointmentDetailView(generics.RetrieveAPIView):
    """
    جزئیات یک نوبت برای صاحب ارایشگاه
    """
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['reservations_list']
    serializer_class = AppointmentBusinessSerializer

    def get_queryset(self):
        return Appointment.objects.filter(
            time_slot__service__business__owner=self.request.user
        )