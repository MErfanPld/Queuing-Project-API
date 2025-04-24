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
    ordering_fields = ['total_price', 'name']
    # filterset_class = PackageFilter

    def perform_create(self, serializer):
        business_id = self.request.data.get('business')
        business = Business.objects.get(id=business_id)
        if business.owner != self.request.user:
            raise PermissionDenied("شما مجوز ایجاد پکیج برای این کسب‌وکار را ندارید.")
        serializer.save()

class PackageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.business.owner != self.request.user:
            raise PermissionDenied("شما مجوز ویرایش این پکیج را ندارید.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.business.owner != self.request.user:
            raise PermissionDenied("شما مجوز حذف این پکیج را ندارید.")
        instance.delete()