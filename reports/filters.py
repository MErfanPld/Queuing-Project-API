import django_filters
from payments.models import Payment
from reservations.models import Appointment

class PaymentFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Payment
        fields = ['start_date', 'end_date', 'method', 'status']


class AppointmentFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='time_slot__date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='time_slot__date', lookup_expr='lte')
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Appointment
        fields = ['start_date', 'end_date', 'status']
