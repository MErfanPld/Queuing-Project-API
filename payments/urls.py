from django.urls import path
from .views import *

urlpatterns = [
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('wallet/transactions/', WalletTransactionsView.as_view(), name='wallet-transactions'),
    path('wallet/<int:appointment_id>/pay_wallet/', PayAppointmentWithWalletAPIView.as_view(),
         name='pay_appointment_wallet'),

    path('cards/number/user/', NumbersCardListView.as_view(), name='numberscard-list'),
    path('cards/number/', NumbersCardListCreateView.as_view(), name='numberscard-list-create'),
    path('cards/number/<int:pk>/', NumbersCardDetailView.as_view(), name='numberscard-detail'),
    path('manual-payments/', ManualPaymentListCreateView.as_view(), name='manualpayment-list-create'),
    path('manual-payments/<int:pk>/', ManualPaymentDetailView.as_view(), name='manualpayment-detail'),
    path('manual-payments/<int:pk>/status/', ManualPaymentStatusUpdateView.as_view(), name='manualpayment-status'),

    #todo ======================== زرین پال ========================
    # path('payment/request/zz/', WalletChargeRequestView.as_view()),
    # path('payment/verify/zz/', WalletChargeVerifyView.as_view()),
]
