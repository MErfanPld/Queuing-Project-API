from django.urls import path
from .views import *

urlpatterns = [
    path('', BusinessListCreateView.as_view(), name='business-list-create'),
    path('<int:pk>/', BusinessRetrieveUpdateDestroyView.as_view(), name='business-detail'),
    
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/', EmployeeRetrieveDestroyView.as_view(), name='employee-detail'),
    
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/create/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='service-detail'),
    
    path('slots/', AvailableTimeSlotListView.as_view(), name='slot-list'),
    path('slots/create/', AvailableTimeSlotCreateView.as_view(), name='slot-create'),
    path('slots/<int:pk>/', AvailableTimeSlotDetailUpdateDeleteView.as_view(), name='slot-detail-update-delete'),
    path('slots/<int:pk>/status/', TimeSlotStatusUpdateView.as_view(), name='slot-status-update'),
    path('slots/by-date-post/', AvailableTimeSlotListCreateView.as_view(), name='slots-by-date-post'),
]