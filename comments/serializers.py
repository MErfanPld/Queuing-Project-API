from rest_framework import serializers
from .models import Comment
from business.models import Business,Service

class CommentSerializer(serializers.ModelSerializer):
    target_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'is_approved', 'created_at', 'updated_at', 'target_name']

    def get_target_name(self, obj):
        if obj.target_type == 'service' and obj.service:
            return obj.service.name
        elif obj.target_type == 'business' and obj.business:
            return obj.business.name
        return '---'

    def validate(self, attrs):
        target_type = attrs.get('target_type') or getattr(self.instance, 'target_type', None)
        service = attrs.get('service') or getattr(self.instance, 'service', None)
        business = attrs.get('business') or getattr(self.instance, 'business', None)

        if target_type == 'service':
            if not service:
                raise serializers.ValidationError({
                    "service": "برای ثبت نظر درباره سرویس باید سرویس را انتخاب کنید."
                })
            attrs['business'] = service.business

        elif target_type == 'business':
            if not business:
                raise serializers.ValidationError({
                    "business": "برای ثبت نظر درباره کسب‌وکار باید کسب‌وکار را انتخاب کنید."
                })
            attrs['service'] = None

        else:
            raise serializers.ValidationError({
                "target_type": "target_type نامعتبر است."
            })

        return attrs
