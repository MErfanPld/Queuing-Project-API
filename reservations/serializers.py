from rest_framework import serializers

from business.models import Employee, Service
from business.serializers import EmployeeSerializer, ServiceSerializer
from .models import Appointment, AvailableTimeSlot



class AppointmentSerializer(serializers.ModelSerializer):
    get_status = serializers.ReadOnlyField()
    service = ServiceSerializer(read_only=True)  # برای GET
    employee = EmployeeSerializer(read_only=True)  # برای GET
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), write_only=True)  # برای POST
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True, required=False)  # برای POST (اختیاری)

    class Meta:
        model = Appointment
        fields = [
            'date', 'time', 'status', 'user',
            'service', 'employee', 'get_status',
            'service_id', 'employee_id'
        ]

    def create(self, validated_data):
        # استخراج `service_id` و `employee_id` و حذف از validated_data
        service = validated_data.pop('service_id')
        employee = validated_data.pop('employee_id', None)

        # ایجاد نوبت با داده‌های دریافتی
        appointment = Appointment.objects.create(service=service, employee=employee, **validated_data)
        return appointment



class AvailableTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTimeSlot
        fields = ['id', 'service', 'date', 'time', 'is_booked']