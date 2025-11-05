from rest_framework import serializers
from .models import Comment
from business.models import Business,Service


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'is_approved', 'created_at', 'updated_at']

    def validate(self, attrs):
        target_type = attrs.get('target_type')
        service = attrs.get('service')
        business = attrs.get('business')

        if target_type == 'service' and not service:
            raise serializers.ValidationError("برای ثبت نظر درباره سرویس باید سرویس را انتخاب کنید.")
        if target_type == 'business' and not business:
            raise serializers.ValidationError("برای ثبت نظر درباره کسب‌وکار باید کسب‌وکار را انتخاب کنید.")
        
        # 🔹 اینجا تغییر اصلی:
        if service and business and service.business != business:
            raise serializers.ValidationError("سرویس انتخاب‌شده متعلق به این کسب‌وکار نیست.")
        
        return attrs
