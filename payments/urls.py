from django.urls import path
from .views import PaymentAPIView

urlpatterns = [
    path('<int:appointment_id>/', PaymentAPIView.as_view(), name='payment-detail'),
    path('', PaymentAPIView.as_view(), name='payment-process'),
]
