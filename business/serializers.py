from rest_framework import serializers

from users.serializers import UserSerializer
from .models import AvailableTimeSlot, Business, Employee, Service
from users.models import User

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer() 

    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')  
        user, created = User.objects.get_or_create(phone_number=user_data['phone_number'], defaults=user_data)

        employee = Employee.objects.create(user=user, **validated_data)
        return employee


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    user = serializers.SerializerMethodField(read_only=True)  # نمایش نام کاربر

    class Meta:
        model = Employee
        fields = ['id', 'user_id', 'user', 'skill']

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": f"{obj.user.first_name} {obj.user.last_name}".strip(),
            "phone": obj.user.phone_number,
        }


class ServiceSerializer(serializers.ModelSerializer):
    business_id = serializers.PrimaryKeyRelatedField(
        queryset=Business.objects.all(), source='business', write_only=True
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='employee', write_only=True
    )

    business = BusinessSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'price',
            'description',
            'duration',
            'business_id',
            'employee_id',
            'business',
            'employee'
        ]


class AvailableTimeSlotSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.SerializerMethodField()
    
    class Meta:
        model = AvailableTimeSlot
        fields = ['id', 'service', 'date', 'start_time', 'end_time', 'is_available']

    def get_start_time(self, obj):
        return obj.start_time.strftime('%H:%M')

    def get_end_time(self, obj):
        return obj.end_time.strftime('%H:%M')
        
        
class TimeSlotStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTimeSlot
        fields = ['is_available']
        
from rest_framework import serializers
from django.db import transaction
from datetime import datetime

from reservations.models import Appointment
from business.models import AvailableTimeSlot


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        service = attrs['service']
        time_slot = attrs['time_slot']

        # 1️⃣ ساعت متعلق به همین سرویس باشد
        if time_slot.service != service:
            raise serializers.ValidationError(
                "این ساعت متعلق به سرویس انتخاب‌شده نیست."
            )

        # 2️⃣ فعال باشد
        if not time_slot.is_available:
            raise serializers.ValidationError(
                "این ساعت غیرفعال است."
            )

        # 3️⃣ تداخل زمانی نداشته باشد
        start_dt = datetime.combine(time_slot.date, time_slot.start_time)
        end_dt = start_dt + service.duration

        conflict = Appointment.objects.filter(
            service=service,
            time_slot__date=time_slot.date,
            status='confirmed',
            time_slot__start_time__lt=end_dt.time(),
            time_slot__start_time__gte=start_dt.time()
        ).exists()

        if conflict:
            raise serializers.ValidationError(
                "این بازه زمانی قبلاً رزرو شده است."
            )

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            appointment = Appointment.objects.create(**validated_data)

            # قفل کردن ساعت
            slot = appointment.time_slot
            slot.is_available = False
            slot.save(update_fields=["is_available"])

            return appointment
