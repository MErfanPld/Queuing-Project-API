from django import forms
from .models import WorkingHours

class WorkingHoursForm(forms.ModelForm):
    class Meta:
        model = WorkingHours
        fields = ['day', 'opening_time', 'closing_time']
        widgets = {
            'opening_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'closing_time': forms.TimeInput(attrs={'class': 'timepicker'}),
        }
