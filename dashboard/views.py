from requests import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from payments.models import Payment
from payments.serializers import PaymentSerializer
from reservations.models import Appointment
from reservations.serializers import AppointmentSerializer

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_superuser or getattr(user, 'is_owner', False):
            appointments = Appointment.objects.all()
            payments = Payment.objects.all()
        else:
            appointments = Appointment.objects.filter(user=user)
            payments = Payment.objects.filter(user=user)

        appointment_data = AppointmentSerializer(appointments, many=True).data
        payment_data = PaymentSerializer(payments, many=True).data

        return Response({
            'appointments': appointment_data,
            'payments': payment_data
        })