from rest_framework import permissions

class HasBusinessPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list']:
            return request.user.has_perm('app.business_list')
        if view.action in ['create']:
            return request.user.has_perm('app.business_create')
        if view.action in ['update', 'partial_update']:
            return request.user.has_perm('app.business_edit')
        if view.action in ['destroy']:
            return request.user.has_perm('app.business_delete')
        return True
