from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from acl.mixins import PermissionMixin
from acl.rest_mixin import RestPermissionMixin
from .models import Package
from .serializers import PackageSerializer
from business.models import Business,Service


class PackageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PackageSerializer

    def get_queryset(self):
        queryset = Package.objects.all()
        business_id = self.request.query_params.get('business_id')
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        return queryset


class PackageCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['packages_create']
    serializer_class = PackageSerializer

    def perform_create(self, serializer):
        business_id = serializer.validated_data['business'].id
        business = Business.objects.get(pk=business_id)
        if business.owner != self.request.user:
            raise PermissionDenied("شما صاحب این کسب‌وکار نیستید.")
        serializer.save()


class PackageDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackageUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ["packages_edit"]
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackageDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,RestPermissionMixin]
    permissions = ['packages_delete']
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
