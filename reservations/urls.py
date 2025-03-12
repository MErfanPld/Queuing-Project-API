from django.urls import path
from .views import *

urlpatterns = [
    path('', AppointmentCreateView.as_view(), name='create_appointment'),
    path('update-appointment-status/', update_appointment_status, name='update_appointment_status'),
    path('get-available-times/', get_available_times, name='get_available_times'),

    path('get-available-times/list', GetAvailableTimesListViewAdmin.as_view(), name='get-available-admin-list'),
    path('get-available-times/create/', GetAvailableTimesCreateViewAdmin.as_view(), name='get-available-admin-create'),
    path('get-available-times/update/<int:pk>/', GetAvailableTimesUpdateViewAdmin.as_view(), name='get-available-admin-update'),
    path('get-available-times/delete/<int:pk>/', GetAvailableTimesDeleteViewAdmin.as_view(), name='get-available-admin-delete'),
    
]
