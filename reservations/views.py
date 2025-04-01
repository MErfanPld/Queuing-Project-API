from rest_framework import generics, status
from .models import Appointment, AvailableTimeSlot
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import AppointmentSerializer, AvailableTimeSlotSerializer
from django.db import transaction


# ============================== Appointment CRUD ==============================
class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:  # بررسی لاگین بودن کاربر
            return Appointment.objects.none()  # جلوگیری از خطای AnonymousUser

        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Appointment.objects.none()

        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

# ============================== Available Time Slot CRUD ==============================
# class AvailableTimeSlotListCreateView(generics.ListCreateAPIView):
#     queryset = AvailableTimeSlot.objects.all()
#     serializer_class = AvailableTimeSlotSerializer
#     permission_classes = [IsAuthenticated]
#
#
# class AvailableTimeSlotDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = AvailableTimeSlot.objects.all()
#     serializer_class = AvailableTimeSlotSerializer
#     permission_classes = [IsAuthenticated]
