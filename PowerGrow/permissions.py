from rest_framework.permissions import BasePermission


class IsAdminUserOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser
