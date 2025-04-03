from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Business, Employee, Service
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

class ServiceSerializer(serializers.ModelSerializer):
    business = BusinessSerializer()  
    employee = EmployeeSerializer()  

    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        business_data = validated_data.pop('business')
        employee_data = validated_data.pop('employee')  
        user_data = employee_data.pop('user')  

        # بررسی اینکه آیا `business` از قبل وجود دارد یا نه
        business, _ = Business.objects.get_or_create(name=business_data['name'], defaults=business_data)

        # بررسی اینکه آیا `user` از قبل وجود دارد یا نه
        user, _ = User.objects.get_or_create(phone_number=user_data['phone_number'], defaults=user_data)

        # بررسی اینکه آیا `employee` از قبل وجود دارد یا نه
        employee, _ = Employee.objects.get_or_create(user=user, defaults=employee_data)

        # ایجاد `Service` با `business` و `employee`
        service = Service.objects.create(business=business, employee=employee, **validated_data)
        return service