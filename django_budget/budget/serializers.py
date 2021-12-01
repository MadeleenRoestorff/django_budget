
from rest_framework import serializers
from . import models


class FixedExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.FixedExpenses

class NecessitiesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Necessities