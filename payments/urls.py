from django.urls import path
from .views import WalletView, WalletTransactionsView,PayAppointmentWithWalletAPIView

urlpatterns = [
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('wallet/transactions/', WalletTransactionsView.as_view(), name='wallet-transactions'),
    path('wallet/<int:appointment_id>/pay_wallet/', PayAppointmentWithWalletAPIView.as_view(),
         name='pay_appointment_wallet'),
    
    #todo ======================== زرین پال ========================
    # path('payment/request/zz/', WalletChargeRequestView.as_view()),
    # path('payment/verify/zz/', WalletChargeVerifyView.as_view()),
]
