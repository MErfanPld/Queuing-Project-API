from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from reservations.models import Appointment
from reservations.serializers import AppointmentSerializer
from .pagination import DshboardPagination
from datetime import date

class TodayAppointmentsDashboardView(ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = DshboardPagination

    def get_queryset(self):
        today = date.today()
        return Appointment.objects.filter(time_slot__date=today).order_by('-time_slot__start_time')
