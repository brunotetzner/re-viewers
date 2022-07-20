from rest_framework import permissions
from rest_framework.views import Request


class HasToken(permissions.BasePermission):
    def has_permission(self, req: Request, _):
        try:
            req.META.get("HTTP_AUTHORIZATION").split(" ")[1]
            return True
        except:
            return False
