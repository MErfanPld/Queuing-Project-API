from rest_framework import serializers

from business.models import Service
from .models import Package
from business.serializers import ServiceSerializer

class PackageSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), many=True
    )
    business_name = serializers.CharField(
        source='business.name', read_only=True
    )

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
            'media_files',
        ]
        extra_kwargs = {
            'business': {'write_only': True},
            'total_price': {'read_only': True},
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.image:
            rep['image'] = instance.image.url
        if instance.media_files:
            rep['media_files'] = instance.media_files.url
        return rep