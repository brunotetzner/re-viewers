from rest_framework import permissions
from rest_framework.views import Request


class HasToken(permissions.BasePermission):
    def has_permission(self, req: Request, _):
        try:
            req.META.get("HTTP_AUTHORIZATION").split(" ")[1]
            return True
        except:
            return False


class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.user_id == request.user.id:
            return True
