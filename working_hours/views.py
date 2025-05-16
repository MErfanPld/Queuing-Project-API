from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from acl.rest_mixin import RestPermissionMixin
from .models import WorkingHours
from .serializers import WorkingHoursSerializer


class WorkingHoursListView(generics.ListAPIView):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer


class WorkingHoursCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['working_hours_create']
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer

class WorkingHoursRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['working_hours_edit','working_hours_delete']
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer