import django_filters
from .models import Package

class PackageFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="total_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="total_price", lookup_expr='lte')
    
    class Meta:
        model = Package
        fields = ['business', 'services']