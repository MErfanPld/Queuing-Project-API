from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import datetime, timedelta, time
from drf_spectacular.utils import extend_schema

from business.models import AvailableTimeSlot, Employee, Service
from reservations.utils import send_cancel_sms, send_reservation_sms
from .models import Appointment
from .serializers import AppointmentSerializer



# ============================== Appointment CRUD ==============================
class AppointmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

    def perform_create(self, serializer):
        appointment = serializer.save(status='confirmed')

        # اطلاعات برای پیامک
        phone = appointment.user.phone_number
        name = appointment.user.first_name or "کاربر"
        date = str(appointment.time_slot.date)
        time = str(appointment.time_slot.start_time)

        # ارسال پیامک رزرو موفق
        send_reservation_sms(phone, name, date, time)


class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)


class AppointmentCancelView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, user=request.user)
        except Appointment.DoesNotExist:
            return Response({"error": "نوبت یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        # اجرای تابع لغو
        appointment.cancel(refund=True)

        # ارسال پیامک لغو موفق
        phone = appointment.user.phone_number
        name = appointment.user.first_name or "کاربر"
        send_cancel_sms(phone, name, appointment.service.name)

        return Response({"message": "نوبت با موفقیت لغو شد."})
    
    
 