from rest_framework import generics

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

class ServiceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['service_list','service_create']
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RestPermissionMixin]
    permissions = ['service_edit','service_delete']
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    