from django.contrib import admin
from . import models


def has_superuser_permission(request):
    """Test if the user making the request is a superuser"""
    return request.user.is_active and request.user.is_superuser


# Only active superuser can access root admin site (default)
admin.site.has_permission = has_superuser_permission


@admin.register(models.Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = [
        field.name for field in models.Budget._meta.fields
    ]


@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = [
        field.name for field in models.Expense._meta.fields
    ]
