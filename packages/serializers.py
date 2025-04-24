from rest_framework import serializers
from .models import Package
from business.serializers import ServiceSerializer


class PackageSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    business_name = serializers.CharField(source='business.name', read_only=True)
    
    class Meta:
        model = Package
        fields = [
            'id',
            'business',
            'business_name',
            'name',
            'services',
            'desc',
            'total_price',
            'image',
            'media_files'
        ]
        extra_kwargs = {
            'business': {'write_only': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        if instance.media_files:
            representation['media_files'] = instance.media_files.url
        return representation
