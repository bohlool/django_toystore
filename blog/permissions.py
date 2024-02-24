from rest_framework.permissions import BasePermission


class IsOwnerOrSuperuserOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET requests
        if request.method in ['GET']:
            return True

        # Allow superusers to perform any action
        if request.user.is_superuser:
            return True

        # Allow users to perform actions on their own posts and comments
        if obj.user == request.user:
            return True

        return False
