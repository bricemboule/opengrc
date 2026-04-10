from rest_framework import serializers
from .models import BudgetPlan, BudgetLine


class BudgetPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetPlan
        fields = "__all__"


class BudgetLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetLine
        fields = "__all__"
