from django.urls import path
from .views import *

urlpatterns = []

dashboard_urls = [
    path('roles/', RolesListView.as_view(), name='roles-list'),
    path('roles/create/', RolesCreateView.as_view(), name='roles-create'),
    path('roles/update/<int:pk>/', RolesUpdateView.as_view(), name='roles-update'),
    path('roles/delete/<int:pk>/', RolesDeleteView.as_view(), name='roles-delete'),

    path('role/user/', RoleUserListView.as_view(), name='role-user-list'),
    path('role/user/create/', RoleUserCreateView.as_view(), name='role-user-create'),
    path('role/user/update/<int:pk>/', RoleUserUpdateView.as_view(), name='role-user-update'),
    path('role/user/delete/<int:pk>/', RoleUserDeleteView.as_view(), name='role-user-delete'),

    path('permission/user/', UserPermissionsListView.as_view(), name='permission-user-list'),
    path('permission/user/create/', UserPermissionsCreateView.as_view(), name='permission-user-create'),
    path('permission/user/update/<int:pk>/', UserPermissionsUpdateView.as_view(), name='permission-user-update'),
    path('permission/user/delete/<int:pk>/', UserPermissionsDeleteView.as_view(), name='permission-user-delete'),
]

urlpatterns += dashboard_urls
