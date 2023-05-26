from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class Role(models.Model):
    """
    Only Super user can create roles
    """
    role_name = models.CharField(
        max_length=36, unique=True
    )
    
    def __str__(self):
        return self.role_name


class User(AbstractUser, PermissionsMixin):
    class StatusFields(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DEACTIVE = 'deactive', 'DeActive'
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    status = models.CharField(
        max_length=12, choices=StatusFields.choices,
        default=StatusFields.ACTIVE
    )
    roles = models.ManyToManyField(Role, related_name='user_roles')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def get_roles(self):
        return ", ".join([role.role_name for role in self.roles.all()])
