
from rest_framework import serializers
from . import models


class FuelLogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.FuelLog
