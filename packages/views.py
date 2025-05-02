from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Package
from .serializers import PackageSerializer
from business.models import Business,Service

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        business_id = self.request.query_params.get('business_id')
        
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        
        return queryset
    
    def perform_create(self, serializer):
        business_id = serializer.validated_data['business'].id
        business = Business.objects.get(pk=business_id)
        
        if business.owner != self.request.user:
            raise PermissionDenied("شما صاحب این کسب‌وکار نیستید.")
        
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def add_services(self, request, pk=None):
        package = self.get_object()
        service_ids = request.data.get('service_ids', [])
        
        if not service_ids:
            return Response(
                {"detail": "سرویس‌ها باید ارسال شوند."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        services = Service.objects.filter(id__in=service_ids)
        package.services.add(*services)
        package.save()  # This will trigger total_price recalculation
        
        return Response(
            PackageSerializer(package).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def remove_services(self, request, pk=None):
        package = self.get_object()
        service_ids = request.data.get('service_ids', [])
        
        if not service_ids:
            return Response(
                {"detail": "سرویس‌ها باید ارسال شوند."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        services = Service.objects.filter(id__in=service_ids)
        package.services.remove(*services)
        package.save()  # This will trigger total_price recalculation
        
        return Response(
            PackageSerializer(package).data,
            status=status.HTTP_200_OK
        )