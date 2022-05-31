from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# Model view sets
router.register(r'budget', views.BudgetViewSet)
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'group', views.GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
