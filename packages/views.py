from rest_framework import generics, permissions, filters

# from packages.filters import PackageFilter
from .models import Package
from .serializers import PackageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from business.models import Business


class PackageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business']
    search_fields = ['name', 'desc']
    ordering_fields = ['name', 'total_price']

    def perform_create(self, serializer):
        business = serializer.validated_data.get('business')
        if business.owner != self.request.user:
            raise PermissionDenied("شما مجاز به ایجاد پکیج برای این کسب‌وکار نیستید.")
        package = serializer.save()
        # بعد از ذخیره، قیمت کل رو حساب کن
        package.total_price = package.calculate_total_price()
        package.save(update_fields=['total_price'])

class PackageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.business.owner != self.request.user:
            raise PermissionDenied("شما مجاز به ویرایش این پکیج نیستید.")
        package = serializer.save()
        # بعد از ویرایش، قیمت کل رو دوباره حساب کن
        package.total_price = package.calculate_total_price()
        package.save(update_fields=['total_price'])

    def perform_destroy(self, instance):
        if instance.business.owner != self.request.user:
            raise PermissionDenied("شما مجاز به حذف این پکیج نیستید.")
        instance.delete()

