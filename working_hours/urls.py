from django.urls import path
from .views import *

urlpatterns = [
    path('', WorkingHoursListCreateView.as_view(), name='working-hours-list-create'),
    path('<int:pk>/', WorkingHoursRetrieveUpdateDestroyView.as_view(), name='working-hours-detail'),
]
