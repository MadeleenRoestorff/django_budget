from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers, models


class BudgetViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
    serializer_class = serializers.BudgetSerializer
    queryset = models.Budget.objects.all().order_by('-id')

    @action(detail=False)
    def count(self, request, *args, **kwargs):
        """Return count for the queryset"""
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.count())


class ExpenseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
    serializer_class = serializers.ExpenseSerializer
    queryset = models.Expense.objects.all().order_by('-id')

    @action(detail=False)
    def count(self, request, *args, **kwargs):
        """Return count for the queryset"""
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.count())
