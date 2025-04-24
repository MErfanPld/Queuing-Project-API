from django.urls import path
from .views import PackageListCreateAPIView, PackageRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PackageListCreateAPIView.as_view(), name='package-list-create'),
    path('<int:pk>/', PackageRetrieveUpdateDestroyAPIView.as_view(), name='package-retrieve-update-destroy'),
    # path('business/<int:business_id>/packages/', PackageListCreateAPIView.as_view(), name='business-packages-list'),
]