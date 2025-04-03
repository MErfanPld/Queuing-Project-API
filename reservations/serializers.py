from rest_framework import serializers

from business.models import Employee, Service
from business.serializers import EmployeeSerializer, ServiceSerializer
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    get_status = serializers.ReadOnlyField()
    service = ServiceSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    employee_name = serializers.SerializerMethodField()
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), write_only=True
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Appointment
        fields = [
            'date', 'time', 'status', 'user',
            'service', 'employee', 'get_status',
            'service_id', 'employee_id', 'employee_name'  
        ]

    def get_employee_name(self, obj):
        if obj.employee and obj.employee.user:
            return obj.employee.user.get_full_name() or obj.employee.user.username
        return None

    def create(self, validated_data):
        service = validated_data.pop('service_id')
        employee = validated_data.pop('employee_id', None)

        #* Create User
        appointment = Appointment.objects.create(service=service, employee=employee, **validated_data)
        return appointment