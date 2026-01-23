from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from datetime import datetime

from reservations.models import Appointment
from business.models import AvailableTimeSlot
from reservations.serializers import AppointmentSerializer
from reservations.utils import send_cancel_sms, send_reservation_sms


# ============================== Appointment CRUD ==============================
class AppointmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

    @transaction.atomic
    def perform_create(self, serializer):
        # ایجاد نوبت
        appointment = serializer.save(status='confirmed')

        # قفل کردن time_slot
        slot = appointment.time_slot
        slot.is_available = False
        slot.save(update_fields=['is_available'])

        # ارسال پیامک رزرو موفق
        phone = appointment.user.phone_number
        name = appointment.user.first_name or "کاربر"
        date = str(appointment.time_slot.date)
        time_ = str(appointment.time_slot.start_time)
        send_reservation_sms(phone, name, date, time_)


class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

    @transaction.atomic
    def perform_update(self, serializer):
        # فقط اجازه تغییر فیلدهای خاص یا تایید وضعیت
        appointment = serializer.save()
        # می‌توانید اینجا چک کنید که time_slot تغییر نکرده باشد یا فعال باشد


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
