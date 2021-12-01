from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# Model view sets
router.register(r'fixedexpenses', views.FixedExpensesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
