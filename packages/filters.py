import django_filters as filters
from django.db.models import Q, Value
from django.db.models.functions import Concat
from unidecode import unidecode


class PackageFilters(filters.FilterSet):
    search = filters.CharFilter(method="search_filter")
    type = filters.CharFilter(method="type_filter")
    limit = filters.CharFilter(method="limit_filter")

    @staticmethod
    def search_filter(qs, name, value):
        qs = qs.filter(
            Q(business__icontains=value) |
            Q(name__icontains=value) |
            Q(total_price__icontains=value)
        ).distinct()
        return qs

    @staticmethod
    def limit_filter(qs, name, value):
        try:
            qs = qs.distinct()[:int(unidecode(value))]
        except:
            pass
        return qs
    