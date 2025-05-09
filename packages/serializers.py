from rest_framework import serializers

from business.models import Business
from .models import Package, Service
from business.serializers import BusinessSerializer,ServiceSerializer

class PackageSerializer(serializers.ModelSerializer):
    business = BusinessSerializer(read_only=True)
    business_id = serializers.PrimaryKeyRelatedField(
        queryset=Business.objects.all(),
        source='business',
        write_only=True,
        required=True
    )
    services = ServiceSerializer(many=True, read_only=True)
    service_ids = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='services',
        many=True,
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Package
        fields = [
            'id',
            'business',
            'business_id',
            'name',
            'desc',
            'total_price',
            'image',
            # 'media_files',
            'services',
            'service_ids',
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_service_ids(self, value):
        if not value:
            raise serializers.ValidationError("حداقل یک سرویس باید انتخاب شود.")
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        else:
            representation['image'] = None
        return representation