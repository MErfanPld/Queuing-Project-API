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
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


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
