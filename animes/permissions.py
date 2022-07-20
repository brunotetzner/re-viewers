from rest_framework import permissions
from rest_framework.views import Request
import ipdb
       
class HasPermission(permissions.BasePermission):
    def has_object_permission(self, req: Request, _):

        ipdb.set_trace()
        public_methods =["GET"]
        
        if req.method in public_methods:
            return True
        
        return req.user.is_superuser