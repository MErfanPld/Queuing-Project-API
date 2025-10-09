from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from acl.mixins import PermissionMixin
from acl.rest_mixin import RestPermissionMixin
from .models import WorkingHours
from .serializers import WorkingHoursSerializer


class WorkingHoursUserListView(generics.ListAPIView):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer


class WorkingHoursListView(PermissionMixin,generics.ListAPIView):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['working_hours_list']

class WorkingHoursCreateView(PermissionMixin,generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['working_hours_create']
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer

class WorkingHoursRetrieveUpdateDestroyView(PermissionMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['working_hours_edit','working_hours_delete']
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer