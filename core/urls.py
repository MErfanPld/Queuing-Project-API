from django.urls import path
from .views import SliderListCreateView, SliderRetrieveUpdateDestroyView

urlpatterns = [
    path("sliders/", SliderListCreateView.as_view(), name="slider-list-create"),
    path("sliders/<int:pk>/", SliderRetrieveUpdateDestroyView.as_view(), name="slider-detail"),
]