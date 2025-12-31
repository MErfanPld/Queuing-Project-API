from rest_framework import serializers

from landing.models import Feature, Plan, PlanFeature


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'key', 'description']


class PlanFeatureSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer()

    class Meta:
        model = PlanFeature
        fields = ['feature', 'value']


class PlanSerializer(serializers.ModelSerializer):
    features = PlanFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = [
            'id',
            'title',
            'price',
            'duration_days',
            'features'
        ]
