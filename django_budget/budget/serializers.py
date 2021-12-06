
from rest_framework import serializers
from . import models


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Budget


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Expense
