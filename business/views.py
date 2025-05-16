from rest_framework import generics

from acl.mixins import PermissionMixin
from acl.rest_mixin import RestPermissionMixin
from .models import Business, Employee, Service
from .serializers import *
from .permissions import *

# Create your views here.


#? ============================= Business CRUD =============================


class BusinessListCreateView(PermissionMixin,generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, RestPermissionMixin]
    permissions = ['business_list','business_create']
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class BusinessRetrieveUpdateDestroyView(PermissionMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, RestPermissionMixin]
    permissions = ['business_edit','business_delete']
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    

#? ============================= Employee CRUD =============================

class EmployeeListView(PermissionMixin,generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_list']
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeCreateView(PermissionMixin,generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_create']
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer

class EmployeeUpdateView(PermissionMixin,generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_edit']
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer

class EmployeeRetrieveDestroyView(PermissionMixin,generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, RestPermissionMixin]
    permissions = ['employee_delete']
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

#? ============================= Services CRUD =============================

class ServiceListCreateView(PermissionMixin,generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, RestPermissionMixin]
    permissions = ['service_list','service_create']
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRetrieveUpdateDestroyView(PermissionMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, RestPermissionMixin]
    permissions = ['service_edit','service_delete']
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    