from django import forms
from .models import Package, Service, PackageReview


class PackageForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="انتخاب سرویس‌ها"
    )

    class Meta:
        model = Package
        fields = ['business', 'name', 'services', 'desc',
                  'total_price', 'image', 'media_files']


class PackageReviewForm(forms.ModelForm):
    class Meta:
        model = PackageReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} ستاره") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
