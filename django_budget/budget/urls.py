from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# Model view sets
router.register(r'fixedexpenses', views.FixedExpensesViewSet)
router.register(r'necessities', views.NecessitiesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
