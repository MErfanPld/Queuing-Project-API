from rest_framework import generics, status
from .models import Appointment, AvailableTimeSlot
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import AppointmentSerializer
from django.db import transaction


# ============================== Appointment CRUD ==============================
class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]  
    permissions = ['reservations_list','reservations_create']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser: 
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)  

class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    permissions = ['reservations_edit','reservations_delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

