from django import forms
from .models import Business, Service, Employee


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = "__all__"


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
