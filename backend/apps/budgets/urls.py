from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BudgetPlanViewSet, BudgetLineViewSet

router = DefaultRouter()
router.register("budget-plans", BudgetPlanViewSet, basename="budget-plans")
router.register("budget-lines", BudgetLineViewSet, basename="budget-lines")

urlpatterns = [path("", include(router.urls))]
