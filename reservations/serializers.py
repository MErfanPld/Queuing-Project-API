from rest_framework import serializers

from business.serializers import EmployeeSerializer, ServiceSerializer
from .models import Appointment, AvailableTimeSlot


class AppointmentSerializer(serializers.ModelSerializer):
    get_status = serializers.ReadOnlyField()
    service = ServiceSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

class AvailableTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTimeSlot
        fields = ['id', 'service', 'date', 'time', 'is_booked']