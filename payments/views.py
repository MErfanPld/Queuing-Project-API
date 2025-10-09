import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from acl.rest_mixin import RestPermissionMixin
from payments.models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import ManualPayment
from .serializers import ManualPaymentSerializer
from django.db.models import Q
from reservations.models import Appointment
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import generics, permissions
from .models import NumbersCard
from .serializers import NumbersCardSerializer


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
    
    


class NumbersCardListView(generics.ListAPIView):
    queryset = NumbersCard.objects.filter(status=True)
    serializer_class = NumbersCardSerializer
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['num_card_list']

class NumbersCardListCreateView(generics.ListCreateAPIView):
    queryset = NumbersCard.objects.all()
    serializer_class = NumbersCardSerializer
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['num_card_list', 'num_card_create']

class NumbersCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NumbersCard.objects.all()
    serializer_class = NumbersCardSerializer
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['num_card_edit','num_card_delete']
    
    
    
    
class ManualPaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = ManualPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ManualPayment.objects.all()
        return ManualPayment.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ManualPaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ManualPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ManualPayment.objects.all()
        return ManualPayment.objects.filter(user=user)


class ManualPaymentStatusUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]  # فقط ادمین

    def patch(self, request, pk):
        payment = get_object_or_404(ManualPayment, pk=pk)
        status_value = request.data.get("status")

        if status_value not in ["pending", "approved", "rejected"]:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        payment.status = status_value
        payment.save(update_fields=["status"])

        return Response({
            "message": "وضعیت پرداخت با موفقیت تغییر کرد.",
            "payment": ManualPaymentSerializer(payment).data
        })

    
    
    
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
