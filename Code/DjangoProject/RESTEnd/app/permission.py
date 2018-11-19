from rest_framework.permissions import BasePermission

from app.models import UserModel


class RequireLoginPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return isinstance(request.user, UserModel)

class ListAllpermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if isinstance(request.user, UserModel):
                return request.user.is_super
            return False
        return True