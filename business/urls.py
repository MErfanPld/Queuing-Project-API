from django.urls import path
from .views import *

urlpatterns = [
    path('', BusinessListCreateView.as_view(), name='business-list-create'),
    path('<int:pk>/', BusinessRetrieveUpdateDestroyView.as_view(), name='business-detail'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/', EmployeeRetrieveDestroyView.as_view(), name='employee-detail'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='service-detail'),
]