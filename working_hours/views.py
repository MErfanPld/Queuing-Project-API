from rest_framework import generics

from .models import WorkingHours
from .serializers import WorkingHoursSerializer


class WorkingHoursListCreateView(generics.ListCreateAPIView):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer


class WorkingHoursRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer