from django.urls import path
from .views import *

urlpatterns = [
    path('', BusinessListCreateView.as_view(), name='business-list-create'),
    path('<int:pk>/', BusinessRetrieveUpdateDestroyView.as_view(), name='business-detail'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-detail'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='service-detail'),
]