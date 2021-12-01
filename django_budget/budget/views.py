from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers, models

class FixedExpensesViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
    serializer_class = serializers.FixedExpensesSerializer
    queryset = models.FixedExpenses.objects.all().order_by('-id')

    @action(detail=False)
    def count(self, request, *args, **kwargs):
        """Return count for the queryset"""
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.count())

class NecessitiesViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
    serializer_class = serializers.NecessitiesSerializer
    queryset = models.Necessities.objects.all().order_by('-id')

    @action(detail=False)
    def count(self, request, *args, **kwargs):
        """Return count for the queryset"""
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.count())