from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet, TransactionViewSet

router = DefaultRouter()
router.register("budgets", BudgetViewSet, basename="budgets")
router.register("transactions", TransactionViewSet, basename="transactions")

urlpatterns = [path("", include(router.urls))]
