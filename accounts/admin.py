from django.contrib import admin

# Register your models here.
from .models import User, Role

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'status', 'email', 'get_roles'
    )
    list_filter = ['status',]
    date_hierarchy = 'timestamp'


admin.site.register(Role)