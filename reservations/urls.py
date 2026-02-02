from django.urls import path
from .views import *


urlpatterns = [
    # ====================== برای مشتری ======================
    path('my-appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('my-appointments/<int:pk>/', AppointmentRetrieveUpdateDestroyView.as_view(), name='appointment-detail'),
    path('my-appointments/<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),

    # ====================== برای صاحب ارایشگاه ======================
    path('business/appointments/', BusinessAppointmentListView.as_view(), name='business-appointment-list'),
    path('business/appointments/<int:pk>/', BusinessAppointmentDetailView.as_view(), name='business-appointment-detail'),
    path('business/appointments/<int:pk>/update/', BusinessAppointmentUpdateView.as_view(), name='business-appointment-update'),
]