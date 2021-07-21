from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = ['email', 'username']