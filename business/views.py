from rest_framework import generics

from acl.mixins import PermissionMixin
from acl.rest_mixin import RestPermissionMixin
from .models import Business, Employee, Service
from .serializers import *
from .permissions import *

# Create your views here.


#? ============================= Business CRUD =============================


class BusinessListCreateView(PermissionMixin,generics.ListCreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasBusinessPermissions]
    permissions = ['business_list','business_create']


class BusinessRetrieveUpdateDestroyView(PermissionMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasBusinessPermissions]
    permissions = ['business_edit','business_delete']
    

#? ============================= Employee CRUD =============================

class EmployeeListView(PermissionMixin,generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permissions = ['employee_list']


class EmployeeCreateView(PermissionMixin,generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer
    permissions = ['employee_create']

class EmployeeUpdateView(PermissionMixin,generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer
    permissions = ['employee_edit']

class EmployeeRetrieveDestroyView(PermissionMixin,generics.RetrieveDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permissions = ['employee_delete']

#? ============================= Services CRUD =============================

class ServiceListCreateView(PermissionMixin,generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permissions = ['service_list','service_create']


class ServiceRetrieveUpdateDestroyView(PermissionMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permissions = ['service_edit','service_delete']
    
    