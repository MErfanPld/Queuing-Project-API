from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView
from .models import Plan
from .serializers import PlanSerializer

class PlanListAPIView(ListAPIView):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .models import Feature
from .serializers import FeatureSerializer

class FeatureAdminViewSet(ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [IsAdminUser]


from .models import PlanFeature
from .serializers import PlanFeatureSerializer

class PlanFeatureAdminViewSet(ModelViewSet):
    queryset = PlanFeature.objects.all()
    serializer_class = PlanFeatureSerializer
    permission_classes = [IsAdminUser]
