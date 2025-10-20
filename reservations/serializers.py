from rest_framework import serializers
from business.models import AvailableTimeSlot, Employee, Service
from business.serializers import AvailableTimeSlotSerializer, EmployeeSerializer, ServiceSerializer
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
    time_slot_id = serializers.PrimaryKeyRelatedField(
        queryset=AvailableTimeSlot.objects.all(), write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'status', 'user', 'service', 'employee', 'get_status', 'employee_name',
            'service_id', 'employee_id', 'time_slot_id'
        ]

    def get_employee_name(self, obj):
        if obj.employee and obj.employee.user:
            return obj.employee.user.get_full_name() or obj.employee.user.username
        return None

    def validate(self, attrs):
        user = self.context['request'].user
        time_slot = attrs.get('time_slot_id')

        # جلوگیری از رزرو تکراری
        if Appointment.objects.filter(user=user, time_slot=time_slot).exists():
            raise serializers.ValidationError("شما قبلاً این بازه زمانی را رزرو کرده‌اید.")
        return attrs

    def create(self, validated_data):
        service = validated_data.pop('service_id')
        employee = validated_data.pop('employee_id', None)
        time_slot = validated_data.pop('time_slot_id')
        user = self.context['request'].user

        # اگر بازه زمانی آزاد است، آن را رزرو کن
        if time_slot.is_available:
            time_slot.is_available = False
            time_slot.save()

        # ایجاد رزرو
        appointment = Appointment.objects.create(
            user=user,
            service=service,
            employee=employee,
            time_slot=time_slot,
            **validated_data
        )
        return appointment
