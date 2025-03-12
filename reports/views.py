import pandas as pd
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from payments.models import Transaction, UserWithdrawalRequests
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView, View
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML, CSS
import os
from datetime import timedelta

# Create your views here.

#? ================================= Transaction Report =================================


class TransactionReportView(ListView):
    permissions = ['transaction_report_list']
    model = Transaction
    template_name = 'reports/transaction_report.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = super().get_queryset()
        date_filter = self.request.GET.get('date_filter')
        today = timezone.now().date()

        if date_filter == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif date_filter == 'yesterday':
            queryset = queryset.filter(
                created_at__date=today - timedelta(days=1))
        elif date_filter == 'past':
            queryset = queryset.filter(
                created_at__date__lt=today - timedelta(days=1))
        return queryset


class TransactionReportPDFView(View):
    def get(self, request, *args, **kwargs):
        date_filter = request.GET.get('date_filter')
        search = request.GET.get('search', '')

        queryset = Transaction.objects.all()
        today = timezone.now().date()

        if date_filter == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif date_filter == 'yesterday':
            queryset = queryset.filter(
                created_at__date=today - timedelta(days=1))
        elif date_filter == 'past':
            queryset = queryset.filter(
                created_at__date__lt=today - timedelta(days=1))

        if search:
            queryset = queryset.filter(
                wallet__user__phone_number__icontains=search)

        transactions = queryset

        template_path = 'reports/transaction_report_pdf.html'
        context = {'transactions': transactions}
        template = get_template(template_path)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transaction_report.pdf"'

        font_path = os.path.join('static', 'fonts', 'Vazir.ttf')
        css = CSS(string=f"""
            @font-face {{
                font-family: 'Vazir';
                src: url('{font_path}');
            }}
            body {{
                font-family: 'Vazir';
                direction: rtl;
                text-align: right;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        """)

        HTML(string=html).write_pdf(response, stylesheets=[css])
        return response


class TransactionReportExcelView(View):
    def get(self, request, *args, **kwargs):
        date_filter = request.GET.get('date_filter')
        search = request.GET.get('search', '')

        queryset = Transaction.objects.all()
        today = timezone.now().date()

        if date_filter == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif date_filter == 'yesterday':
            queryset = queryset.filter(
                created_at__date=today - timedelta(days=1))
        elif date_filter == 'past':
            queryset = queryset.filter(
                created_at__date__lt=today - timedelta(days=1))

        if search:
            queryset = queryset.filter(
                wallet__user__phone_number__icontains=search)

        data = []
        for transaction in queryset:
            data.append({
                'کاربر': transaction.wallet.user.phone_number,
                'مقدار': transaction.amount,
                'تاریخ': transaction.created_at.replace(tzinfo=None),
            })

        df = pd.DataFrame(data)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=transaction_report.xlsx'
        df.to_excel(response, index=False)
        return response


#? ================================= UserWithdrawalRequests Report =================================

class UserWithdrawalRequestsReportView(ListView):
    permissions = ['withdrawal_report_list']
    model = UserWithdrawalRequests
    template_name = 'reports/user_withdrawal_requests_report.html'
    context_object_name = 'user_withdrawal_requests'

    def get_queryset(self):
        queryset = super().get_queryset()
        date_filter = self.request.GET.get('date_filter')
        today = timezone.now().date()

        if date_filter == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif date_filter == 'yesterday':
            queryset = queryset.filter(
                created_at__date=today - timedelta(days=1))
        elif date_filter == 'past':
            queryset = queryset.filter(
                created_at__date__lt=today - timedelta(days=1))

        return queryset


class UserWithdrawalRequestsReportPDFView(View):
    def get(self, request, *args, **kwargs):
        date_filter = request.GET.get('date_filter')
        search = request.GET.get('search', '')

        queryset = UserWithdrawalRequests.objects.all()
        today = timezone.now().date()

        if date_filter == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif date_filter == 'yesterday':
            queryset = queryset.filter(
                created_at__date=today - timedelta(days=1))
        elif date_filter == 'past':
            queryset = queryset.filter(
                created_at__date__lt=today - timedelta(days=1))

        if search:
            queryset = queryset.filter(
                wallet__user__phone_number__icontains=search)

        user_withdrawal_requests = queryset

        template_path = 'reports/user_withdrawal_requests_report_pdf.html'
        context = {'user_withdrawal_requests': user_withdrawal_requests}
        template = get_template(template_path)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="user_withdrawal_requests.pdf"'

        font_path = os.path.join('static', 'fonts', 'Vazir.ttf')
        css = CSS(string=f"""
            @font-face {{
                font-family: 'Vazir';
                src: url('{font_path}');
            }}
            body {{
                font-family: 'Vazir';
                direction: rtl;
                text-align: right;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        """)

        HTML(string=html).write_pdf(response, stylesheets=[css])
        return response


class UserWithdrawalRequestsReportExcelView(View):
    def get(self, request, *args, **kwargs):
        date_filter = request.GET.get('date_filter')
        search = request.GET.get('search', '')

        queryset = UserWithdrawalRequests.objects.all()
        today = timezone.now().date()

        if date_filter == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif date_filter == 'yesterday':
            queryset = queryset.filter(
                created_at__date=today - timedelta(days=1))
        elif date_filter == 'past':
            queryset = queryset.filter(
                created_at__date__lt=today - timedelta(days=1))

        if search:
            queryset = queryset.filter(
                wallet__user__phone_number__icontains=search)

        data = []
        for item in queryset:
            data.append({
                'کاربر': item.user,
                'نوبت': item.appointment,
                'وضعیت': item.status,
                'تاریخ': item.created_at.replace(tzinfo=None),
            })

        df = pd.DataFrame(data)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=user_withdrawal_requests_reports.xlsx'
        df.to_excel(response, index=False)
        return response
