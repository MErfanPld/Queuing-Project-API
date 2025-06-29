import requests
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
        amount = request.data.get('balance')
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
    
    
    
    
    
#todo ======================== زرین پال ========================

# SANDBOX_MERCHANT_ID = 'e2b0797e-7e28-11e5-b5eb-005056a205be'  # مخصوص تست
# BASE_URL = 'https://sandbox.zarinpal.com/pg/v4'
# STARTPAY_URL = 'https://sandbox.zarinpal.com/pg/StartPay'

# class WalletChargeRequestView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         amount = int(request.data.get('amount') or request.data.get('balance') or 0)
#         if amount <= 0:
#             return Response({'error': 'مبلغ معتبر نیست'}, status=400)

#         callback_url = 'http://localhost:8000/payment/verify/zz/'

#         data = {
#             "merchant_id": SANDBOX_MERCHANT_ID,
#             "amount": amount,
#             "callback_url": callback_url,
#             "description": "شارژ کیف پول",
#         }

#         response = requests.post(f'{BASE_URL}/payment/request.json', json=data)
#         result = response.json()

#         if result.get('data') and result['data'].get('code') == 100:
#             authority = result['data']['authority']
#             return Response({'payment_url': f"{STARTPAY_URL}/{authority}"})
#         else:
#             return Response({'error': result.get('errors', 'خطا در ارتباط با زرین‌پال')}, status=400)


# class WalletChargeVerifyView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         authority = request.GET.get('Authority')
#         status = request.GET.get('Status')

#         if status != 'OK':
#             return Response({'error': 'پرداخت توسط کاربر لغو شد'}, status=400)

#         # مقدار مبلغ واقعی رو بهتره از جایی ذخیره‌شده بخونی (مثل سشن یا مدل موقت)
#         amount = 1000  # فقط برای تست!

#         data = {
#             "merchant_id": SANDBOX_MERCHANT_ID,
#             "amount": amount,
#             "authority": authority,
#         }

#         response = requests.post(f'{BASE_URL}/payment/verify.json', json=data)
#         result = response.json()

#         if result.get('data') and result['data'].get('code') == 100:
#             wallet, _ = Wallet.objects.get_or_create(user=request.user)
#             wallet.increase(amount)

#             Transaction.objects.create(
#                 wallet=wallet,
#                 amount=amount,
#                 type='DEPOSIT',
#                 status='SUCCESS',
#                 reference_id=result['data']['ref_id']
#             )

#             return Response({'message': 'پرداخت موفق', 'ref_id': result['data']['ref_id']})
#         else:
#             return Response({'error': 'تأیید پرداخت ناموفق'}, status=400)
