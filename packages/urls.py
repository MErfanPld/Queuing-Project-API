from django.urls import path
from .views import PackageListView, PackageDetailView, AddReviewView, PackageListViewAdmin, PackageCreateViewAdmin, PackageUpdateViewAdmin, PackageDeleteViewAdmin, PackageReviewListViewAdmin, PackageReviewDeleteViewAdmin

app_name = 'packages'

urlpatterns = [
    path('', PackageListView.as_view(), name='package_list'),
    path('<int:pk>/', PackageDetailView.as_view(), name='package_detail'),
    path('<int:pk>/review/', AddReviewView.as_view(), name='package_add_review'),

    path('list', PackageListViewAdmin.as_view(), name='package-admin-list'),
    path('create/', PackageCreateViewAdmin.as_view(), name='package-create'),
    path('update/<int:pk>/', PackageUpdateViewAdmin.as_view(), name='package-update'),
    path('delete/<int:pk>/', PackageDeleteViewAdmin.as_view(), name='package-delete'),
    
    path('delete/review/<int:pk>/', PackageReviewDeleteViewAdmin.as_view(), name='package-delete-review'),
    path('list/review/', PackageReviewListViewAdmin.as_view(), name='package-list-review'),
]
