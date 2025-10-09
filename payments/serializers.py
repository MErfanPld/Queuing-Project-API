from rest_framework import serializers
from payments.models import *

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'status', 'created_at', 'reservation']
        depth = 1

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        
class NumbersCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumbersCard
        fields = "__all__"

class ManualPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualPayment
        fields = "__all__"
        read_only_fields = ['status', 'created_at', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)