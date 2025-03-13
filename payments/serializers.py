from rest_framework import serializers
from decimal import Decimal
from .models import Appointment, Wallet, Transaction


class PaymentSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'service', 'price', 'status']

    def get_price(self, obj):
        return obj.service.price  # دریافت قیمت سرویس مرتبط با نوبت


class PaymentProcessSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField()

    def validate_appointment_id(self, value):
        """ بررسی اینکه نوبت معتبر باشد """
        if not Appointment.objects.filter(id=value).exists():
            raise serializers.ValidationError("نوبت یافت نشد.")
        return value

    def process_payment(self):
        """ پردازش پرداخت و بروزرسانی کیف پول """
        appointment_id = self.validated_data['appointment_id']
        appointment = Appointment.objects.get(id=appointment_id)
        service = appointment.service

        # دریافت یا ایجاد کیف پول کاربر
        wallet, created = Wallet.objects.get_or_create(user=appointment.user)

        # انجام تراکنش و بروزرسانی کیف پول
        amount = Decimal(service.price)
        Transaction.objects.create(wallet=wallet, amount=amount)
        wallet.balance += amount
        wallet.save()

        # بروزرسانی وضعیت نوبت
        appointment.status = 'confirmed'
        appointment.save()

        return appointment
