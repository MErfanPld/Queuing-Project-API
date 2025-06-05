from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from payments.models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from reservations.models import Appointment
from django.core.exceptions import ValidationError
from django.db import transaction

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'مبلغ وارد نشده است'}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return Response({'error': 'مبلغ معتبر نیست'}, status=400)

        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        wallet.increase(amount)

        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            type='DEPOSIT',
            status='SUCCESS'
        )

        return Response({'message': 'شارژ با موفقیت انجام شد'}, status=status.HTTP_200_OK)


class WalletTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        transactions = Transaction.objects.filter(wallet=wallet).order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class PayAppointmentWithWalletAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id, user=request.user)

        if appointment.status != 'pending':
            return Response({"error": "رزرو قبلاً پرداخت یا تایید شده است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment.pay_with_wallet()
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "پرداخت با کیف پول موفقیت‌آمیز بود."})