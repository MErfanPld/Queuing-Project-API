from django.urls import path
from .views import TodayAppointmentsDashboardView

urlpatterns = [
    path('today-appointments/', TodayAppointmentsDashboardView.as_view(), name='today-appointments'),
]
