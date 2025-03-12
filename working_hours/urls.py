from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkingHoursListView.as_view(), name='working_hours'),

    path('list', views.WorkingHoursListViewAdmin.as_view(), name='working-hours-list'),
    path('create/', views.WorkingHoursCreateViewAdmin.as_view(), name='working-hours-create'),
    path('update/<int:pk>/', views.WorkingHoursUpdateViewAdmin.as_view(), name='working-hours-update'),
    path('delete/<int:pk>/', views.WorkingHoursDeleteViewAdmin.as_view(), name='working-hours-delete'),
]
