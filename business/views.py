from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from acl.mixins import PermissionMixin
from acl.rest_mixin import RestPermissionMixin
from .models import Business, Employee, Service
from .serializers import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.


#? ============================= Business CRUD =============================


class BusinessListCreateView(PermissionMixin,generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['business_list','business_create']
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class BusinessRetrieveUpdateDestroyView(PermissionMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['business_edit','business_delete']
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    

#? ============================= Employee CRUD =============================

class EmployeeListView(PermissionMixin,generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    permissions = ['employee_list']
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeCreateView(PermissionMixin,generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_create']
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer

class EmployeeUpdateView(PermissionMixin,generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_edit']
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer

class EmployeeRetrieveDestroyView(PermissionMixin,generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_delete']
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

#? ============================= Services CRUD =============================

# class ServiceListCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     permissions = ['service_list','service_create']
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer

class ServiceListView(PermissionMixin,generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permissions = ['service_list']  

class ServiceCreateView(PermissionMixin,generics.CreateAPIView):
    permission_classes = [IsAuthenticated,RestPermissionMixin]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permissions = ['service_create']


class ServiceRetrieveUpdateDestroyView(PermissionMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    permissions = ['service_edit','service_delete']
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    

#? ============================= Available Time Slot CRUD =============================
class AvailableTimeSlotListView(PermissionMixin,generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    permissions = ['time_slot_list']
    queryset = AvailableTimeSlot.objects.all()
    serializer_class = AvailableTimeSlotSerializer


class AvailableTimeSlotCreateView(PermissionMixin,generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    permissions = ['time_slot_create']
    queryset = AvailableTimeSlot.objects.all()
    serializer_class = AvailableTimeSlotSerializer


class AvailableTimeSlotDetailUpdateDeleteView(PermissionMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    permissions = ['time_slot_update', 'time_slot_delete']

    queryset = AvailableTimeSlot.objects.all()
    serializer_class = AvailableTimeSlotSerializer
    
    
class TimeSlotStatusUpdateView(PermissionMixin,generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AvailableTimeSlot.objects.all()
    serializer_class = TimeSlotStatusUpdateSerializer
    
    
class AvailableTimeSlotListCreateView(PermissionMixin,generics.ListCreateAPIView):
    serializer_class = AvailableTimeSlotSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        service_id = self.request.query_params.get('service_id')
        date = self.request.query_params.get('date')

        queryset = AvailableTimeSlot.objects.filter(is_available=True)

        if service_id:
            queryset = queryset.filter(service_id=service_id)
        if date:
            queryset = queryset.filter(date=date)

        return queryset