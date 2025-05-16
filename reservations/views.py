from rest_framework import generics, status

from acl.mixins import PermissionMixin
from acl.rest_mixin import RestPermissionMixin
from .models import Appointment, AvailableTimeSlot
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import AppointmentSerializer
from django.db import transaction


# ============================== Appointment CRUD ==============================
class AppointmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser: 
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)  

class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

