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


class BusinessListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['business_list','business_create']
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class BusinessRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['business_edit','business_delete']
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    

#? ============================= Employee CRUD =============================

class EmployeeListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_list']
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_create']
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer

class EmployeeUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_edit']
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer

class EmployeeRetrieveDestroyView(generics.RetrieveDestroyAPIView):
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

class ServiceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permissions = ['service_list']  

class ServiceCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permissions = ['service_create']


class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    permissions = ['service_edit','service_delete']
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    

#? ============================= Available Time Slot CRUD =============================
class AvailableTimeSlotCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AvailableTimeSlot.objects.all()
    serializer_class = AvailableTimeSlotSerializer


class AvailableTimeSlotDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AvailableTimeSlot.objects.all()
    serializer_class = AvailableTimeSlotSerializer
    
    
class TimeSlotStatusUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AvailableTimeSlot.objects.all()
    serializer_class = TimeSlotStatusUpdateSerializer
    
    
class AvailableTimeSlotListCreateView(generics.ListCreateAPIView):
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