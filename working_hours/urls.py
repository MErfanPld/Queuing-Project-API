from django.urls import path
from .views import *

urlpatterns = [
    path('user/', WorkingHoursUserListView.as_view(), name='working-hours-list-user'),
    path('', WorkingHoursListView.as_view(), name='working-hours-list'),
    path('create/', WorkingHoursCreateView.as_view(), name='working-hours-create'),
    path('<int:pk>/', WorkingHoursRetrieveUpdateDestroyView.as_view(), name='working-hours-detail'),
]
