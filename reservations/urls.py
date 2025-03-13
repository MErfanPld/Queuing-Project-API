from django.urls import path
from .views import *

urlpatterns = [
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentRetrieveUpdateDestroyView.as_view(), name='appointment-detail'),

    # path('available-slots/', AvailableTimeSlotListCreateView.as_view(), name='available-slot-list'),
    # path('available-slots/<int:pk>/', AvailableTimeSlotDetailView.as_view(), name='available-slot-detail'),
]