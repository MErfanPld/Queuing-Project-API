from django.urls import path
from .views import *

urlpatterns = [
    path('transaction-report/', TransactionReportView.as_view(), name='transaction_report'),
    path('transaction-report/pdf/', TransactionReportPDFView.as_view(), name='transaction_report_pdf'),
    path('transaction-report/excel/', TransactionReportExcelView.as_view(), name='transaction_report_excel'),

    path('user-withdrawal-report/', UserWithdrawalRequestsReportView.as_view(), name='withdrawal_report'),
    path('user-withdrawal-report/pdf/', UserWithdrawalRequestsReportPDFView.as_view(), name='withdrawal_report_pdf'),
    path('user-withdrawal-report/excel/', UserWithdrawalRequestsReportExcelView.as_view(), name='withdrawal_report_excel'),
]

