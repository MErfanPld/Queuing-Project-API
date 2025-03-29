from rest_framework import serializers

from business.serializers import EmployeeSerializer, ServiceSerializer
from .models import Appointment, AvailableTimeSlot


class AppointmentSerializer(serializers.ModelSerializer):
    get_status = serializers.ReadOnlyField()
    service = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'status', 'user', 'service', 'employee', 'get_status']

    def get_service(self, obj):
        return {'name': obj.service.name} if obj.service else None

    def get_employee(self, obj):
        if obj.employee:
            return {
                'first_name': obj.employee.user.first_name,
                'last_name': obj.employee.user.last_name,
                'skill': obj.employee.skill
            }
        return None



class AvailableTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTimeSlot
        fields = ['id', 'service', 'date', 'time', 'is_booked']