from django.urls import path
from .views import *
from django.views.generic import TemplateView
from .views import SomeErrorPageView

urlpatterns = [
    path('payment/<int:appointment_id>/', PaymentView.as_view(), name='payment'),
    path('process-payment/', ProcessPaymentView.as_view(), name='process_payment'),

    
    path('appointment/success/<int:appointment_id>/', TemplateView.as_view(
        template_name='appointment_success.html'), name='appointment_success'),
    
    path('wallet/add-funds/',
        TemplateView.as_view(template_name='payments/add_funds.html'), name='add_funds'),
    
    path('error/', SomeErrorPageView.as_view(), name='some_error_page'),

    path('wallet/create/', CreateWalletView.as_view(), name='create_wallet'),
    path('wallet/success/', WalletSuccess.as_view(), name='wallet_success'),
    path('wallet/add-funds/', AddFundsView.as_view(), name='add_funds'),
]
