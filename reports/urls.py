from django.urls import path
from .views import *

urlpatterns = [
    path('financial/', FinancialReportAPIView.as_view(), name='financial-report'),
    path('appointments/', AppointmentReportAPIView.as_view(), name='appointment-report'),
]

