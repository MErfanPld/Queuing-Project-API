from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('admin/features', FeatureAdminViewSet)
router.register('admin/plan-features', PlanFeatureAdminViewSet)

urlpatterns = [
    path('plans/', PlanListAPIView.as_view()),
    path('', include(router.urls)),
    path('subscription/', SubscriptionDetailAPIView.as_view(), name='subscription-detail')
]
