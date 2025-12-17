from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.utils.dateparse import parse_datetime
from payments.models import Transaction, Payment
from django.db.models import Sum, Count
from reports.filters import *
from reservations.models import Appointment
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.utils.dateparse import parse_date

class FinancialReportAPIView(APIView):
    permission_classes = [IsAdminUser]
    filterset_class = PaymentFilter

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        format_type = request.GET.get('format')  # اگر بخوای خروجی pdf بدی

        payments = Payment.objects.select_related('user', 'reservation').filter(status='SUCCESS')
        transactions = Transaction.objects.select_related('wallet__user', 'reservation').filter(status='SUCCESS')

        if start_date:
            payments = payments.filter(created_at__gte=parse_datetime(start_date))
            transactions = transactions.filter(created_at__gte=parse_datetime(start_date))
        if end_date:
            payments = payments.filter(created_at__lte=parse_datetime(end_date))
            transactions = transactions.filter(created_at__lte=parse_datetime(end_date))

        total_income = payments.aggregate(total=Sum('amount'))['total'] or 0
        total_wallet = payments.filter(method='WALLET').aggregate(total=Sum('amount'))['total'] or 0
        total_gateway = payments.filter(method='GATEWAY').aggregate(total=Sum('amount'))['total'] or 0

        # ساخت PDF
        if format_type == 'pdf':
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)

            # فونت فارسی (نیاز به فایل فونت در پوشه پروژه)
            try:
                pdfmetrics.registerFont(TTFont('IRANSans', 'fonts/IRANSans.ttf'))
                p.setFont('IRANSans', 14)
            except:
                p.setFont('Helvetica', 12)

            p.drawString(100, 800, f"گزارش مالی ناراتایم")
            p.drawString(100, 780, f"مجموع درآمد: {total_income}")
            p.drawString(100, 760, f"پرداخت با کیف پول: {total_wallet}")
            p.drawString(100, 740, f"پرداخت با درگاه: {total_gateway}")

            y = 700
            for pay in payments:
                p.drawString(100, y, f"{pay.user.username} - {pay.amount} - {pay.method} - {pay.created_at.strftime('%Y-%m-%d')}")
                y -= 20
                if y < 100:
                    p.showPage()
                    y = 800

            p.save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='financial_report.pdf')

        # خروجی JSON (جزئیات پرداخت‌ها)
        payment_list = [
            {
                "user": pay.user.username,
                "amount": pay.amount,
                "method": pay.method,
                "date": pay.created_at.strftime('%Y-%m-%d %H:%M'),
                "reservation": str(pay.reservation) if pay.reservation else None,
            }
            for pay in payments
        ]

        return Response({
            'total_income': total_income,
            'wallet_payments': total_wallet,
            'gateway_payments': total_gateway,
            'successful_transactions': transactions.count(),
            'payments': payment_list
        })

class AppointmentReportAPIView(APIView):
    permission_classes = [IsAdminUser]
    filterset_class = AppointmentFilter

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        format_type = request.GET.get('format')  # 'pdf' برای خروجی PDF

        appointments = Appointment.objects.select_related('user', 'service', 'employee', 'time_slot').all()

        if start_date:
            appointments = appointments.filter(time_slot__date__gte=parse_date(start_date))
        if end_date:
            appointments = appointments.filter(time_slot__date__lte=parse_date(end_date))

        # اطلاعات کامل نوبت‌ها برای JSON
        appointment_list = []
        for app in appointments:
            appointment_list.append({
                "user": app.user.get_full_name(),
                "service": str(app.service),
                "employee": str(app.employee) if app.employee else None,
                "time_slot": str(app.time_slot),
                "status": app.get_status,
            })

        if format_type == 'pdf':
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)

            try:
                pdfmetrics.registerFont(TTFont('IRANSans', 'fonts/IRANSans.ttf'))
                p.setFont('IRANSans', 14)
            except:
                p.setFont('Helvetica', 12)

            p.drawString(100, 800, "گزارش نوبت‌های ناراتایم")
            y = 780
            for app in appointment_list:
                line = f"{app['user']} - {app['service']} - {app['employee'] or '-'} - {app['time_slot']} - {app['status']}"
                p.drawString(50, y, line)
                y -= 20
                if y < 100:
                    p.showPage()
                    try:
                        p.setFont('IRANSans', 14)
                    except:
                        p.setFont('Helvetica', 12)
                    y = 800

            p.save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='appointment_report.pdf')

        return Response({
            'total_appointments': appointments.count(),
            'appointments': appointment_list
        })
        
        
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q

from business.models import Service
from reservations.models import Appointment

class TopServicesByReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not (user.is_superuser or getattr(user, 'is_owner', False)):
            return Response({"error": "دسترسی ندارید"}, status=403)

        # شمارش نوبت‌های تایید شده هر سرویس
        services = Service.objects.annotate(
            confirmed_count=Count('appointments', filter=Q(appointments__status='confirmed'))
        ).order_by('-confirmed_count')

        report = [
            {
                'service_id': s.id,
                'service_name': s.name,
                'confirmed_appointments': s.confirmed_count
            } for s in services
        ]

        return Response({
            'top_by_reservations': report[:5],  # ۵ سرویس پرفروش
            'full_report': report
        })
