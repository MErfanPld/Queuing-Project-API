from rest_framework import generics
from .models import Business, Employee, Service
from .serializers import *

# Create your views here.


#? ============================= Business CRUD =============================


class BusinessListCreateView(generics.ListCreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permissions = ['business_list','business_create']


class BusinessRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permissions = ['business_edit','business_delete']
    

#? ============================= Employee CRUD =============================

class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permissions = ['employee_list']


class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer
    permissions = ['employee_create']

class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateUpdateSerializer
    permissions = ['employee_edit']

class EmployeeRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permissions = ['employee_delete']

#? ============================= Services CRUD =============================

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permissions = ['service_list','service_create']


class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permissions = ['service_edit','service_delete']
    
    