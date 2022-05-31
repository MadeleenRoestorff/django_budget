from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Group

from . import serializers, models
import json


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


class UserViewSet(viewsets.ModelViewSet):
    """
    View for the built-in Django user model.
    """
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [filters.OrderingFilter]


class GroupViewSet(viewsets.ModelViewSet):
    """
    View for the built-in Django group (of users) model.
    """
    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
