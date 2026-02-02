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

        if Appointment.objects.filter(user=user, time_slot=time_slot).exists():
            raise serializers.ValidationError("شما قبلاً این بازه زمانی را رزرو کرده‌اید.")
        return attrs

    def create(self, validated_data):
        # همه فیلدهای کاستوم رو pop کن
        service = validated_data.pop('service_id')
        employee = validated_data.pop('employee_id', None)
        time_slot = validated_data.pop('time_slot_id')
        user = self.context['request'].user
        
        # اگه user از قبل توی validated_data بود، پاکش کن
        validated_data.pop('user', None)

        if not time_slot.is_available:
            raise serializers.ValidationError("این بازه قبلاً رزرو شده")

        time_slot.is_available = False
        time_slot.save()

        appointment = Appointment.objects.create(
            user=user,
            service=service,
            employee=employee,
            time_slot=time_slot,
            **validated_data
        )
        return appointment


# ============================== جدید: برای صاحب ارایشگاه ==============================
class AppointmentBusinessSerializer(serializers.ModelSerializer):
    """سریالایزر برای نمایش نوبت‌ها به صاحب ارایشگاه"""
    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()
    service_name = serializers.CharField(source='service.name')
    employee_name = serializers.SerializerMethodField()
    date = serializers.DateField(source='time_slot.date')
    start_time = serializers.TimeField(source='time_slot.start_time')
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'status', 'customer_name', 'customer_phone',
            'service_name', 'employee_name', 'date', 'start_time', 'end_time',
            'reminder_sent'
        ]

    def get_customer_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_customer_phone(self, obj):
        return obj.user.phone_number

    def get_employee_name(self, obj):
        if obj.employee and obj.employee.user:
            return obj.employee.user.get_full_name() or obj.employee.user.username
        return "بدون کارمند"

    def get_end_time(self, obj):
        from datetime import datetime, timedelta
        
        # دریافت duration از سرویس
        duration = obj.service.duration
        
        # اگه duration None باشه، مقدار پیش‌فرض بذار
        if duration is None:
            duration = timedelta(minutes=30)
        
        # اگه duration timedelta نباشه، تبدیلش کن
        if not isinstance(duration, timedelta):
            try:
                # اگه به صورت رشته باشه (مثل "00:30:00")
                if isinstance(duration, str):
                    parts = duration.split(':')
                    if len(parts) == 3:
                        h, m, s = map(int, parts)
                        duration = timedelta(hours=h, minutes=m, seconds=s)
                    else:
                        duration = timedelta(minutes=30)
                else:
                    # اگه نوع دیگه‌ای باشه
                    duration = timedelta(minutes=30)
            except:
                duration = timedelta(minutes=30)
        
        # محاسبه زمان پایان
        start_datetime = datetime.combine(obj.time_slot.date, obj.time_slot.start_time)
        end_datetime = start_datetime + duration
        
        return end_datetime.time().strftime("%H:%M")