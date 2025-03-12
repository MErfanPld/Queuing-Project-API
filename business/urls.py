from django.urls import path
from .views import *

urlpatterns = [
    path('', BusinessListView.as_view(), name='business-list'),
    path('create/', BusinessCreateView.as_view(), name='business-create'),
    path('update/<int:pk>/', BusinessUpdateView.as_view(), name='business-update'),
    path('delete/<int:pk>/', BusinessDeleteView.as_view(), name='business-delete'),
    
    path('service/', ServiceListView.as_view(), name='service-list'),
    path('service/create/', ServiceCreateView.as_view(), name='service-create'),
    path('service/update/<int:pk>/', ServiceUpdateView.as_view(), name='service-update'),
    path('service/delete/<int:pk>/', ServiceDeleteView.as_view(), name='service-delete'),
    path('service/paid/', PaidServicesView.as_view(), name='paid_services'),
    
    path('employee/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee-delete'),
    
]
