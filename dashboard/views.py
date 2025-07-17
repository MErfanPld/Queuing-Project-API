from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers import PaymentSerializer
from reservations.models import Appointment
from reservations.serializers import AppointmentSerializer

User = get_user_model()


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now().date()

        if user.is_superuser or getattr(user, 'is_owner', False):
            # 🟦 داشبورد ادمین / مالک
            appointments = Appointment.objects.all()
            payments = Payment.objects.all()
            users = User.objects.filter(is_active=True)

            today_appointments = appointments.filter(time_slot__date=now)
            today_income = payments.filter(created_at__date=now).aggregate(total=Sum('amount'))['total'] or 0
            week_income = payments.filter(created_at__gte=now - timedelta(days=7)).aggregate(total=Sum('amount'))['total'] or 0
            month_income = payments.filter(created_at__gte=now - timedelta(days=30)).aggregate(total=Sum('amount'))['total'] or 0

            latest_payments = PaymentSerializer(payments.order_by('-created_at')[:5], many=True).data
            new_users = users.order_by('-created_at')[:5].values('id', 'phone_number', 'created_at')

            return Response({
                'type': 'admin',
                'total_appointments': appointments.count(),
                'today_appointments': today_appointments.count(),
                'income': {
                    'today': today_income,
                    'week': week_income,
                    'month': month_income
                },
                'active_users': users.count(),
                'recent_payments': latest_payments,
                'new_users': list(new_users),
            })

        else:
            # 🟩 داشبورد کاربر عادی
            appointments = Appointment.objects.filter(user=user).order_by('-status')
            payments = Payment.objects.filter(user=user).order_by('-created_at')

            total_appointments = appointments.count()
            next_appointment = appointments.filter(time_slot__date__gte=now).order_by('time_slot__date').first()
            last_5_appointments = AppointmentSerializer(appointments[:5], many=True).data
            last_5_payments = PaymentSerializer(payments[:5], many=True).data
            unpaid_payments = payments.filter(status='unpaid').count()

            return Response({
                'type': 'user',
                'total_appointments': total_appointments,
                'next_appointment': AppointmentSerializer(next_appointment).data if next_appointment else None,
                'last_appointments': last_5_appointments,
                'last_payments': last_5_payments,
                'unpaid_reminder': unpaid_payments > 0,
            })
