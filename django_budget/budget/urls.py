from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# Model view sets
router.register(r'budget', views.BudgetViewSet)
router.register(r'expenses', views.ExpenseViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
