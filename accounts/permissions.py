from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminUserPermission(permissions.IsAdminUser):

    def has_permission(self, request, view):
        return 'Admin' in list(request.user.roles.all().values_list('role_name', flat=True))
