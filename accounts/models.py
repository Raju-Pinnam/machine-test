from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField


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
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    roles = ArrayField(
        models.IntegerField(),
        blank=True, default=list
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email