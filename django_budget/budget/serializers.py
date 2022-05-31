
from rest_framework import serializers
from . import models
from django.contrib.auth.models import User, Group


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Budget


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Expense


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the built-in Django user model.
    """
    class Meta:
        model = User
        exclude = ["password"]


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the built-in Django group (of users) model.
    """
    class Meta:
        model = Group
        fields = "__all__"
