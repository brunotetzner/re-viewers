from rest_framework.permissions import BasePermission
from rest_framework.views import Request


class UserPermission(BasePermission):
    def has_permission(self, req: Request, _):
        user_methods = {"GET", "PATCH", "DELETE"}
        if req.method in user_methods:
            return req.user.is_active

        return True


class AdminPermission(BasePermission):
    def has_permission(self, req: Request, _):
        admin_methods = {"GET", "DELETE"}
        if req.method in admin_methods:
            return req.user.is_superuser

        return True
