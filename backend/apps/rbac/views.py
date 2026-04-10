from django.contrib.auth.models import Permission
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Role
from .serializers import RoleSerializer, PermissionSerializer

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.prefetch_related("permissions").all().order_by("name")
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name", "code"]

class PermissionListView(ListAPIView):
    queryset = Permission.objects.select_related("content_type").all().order_by("content_type__app_label", "codename")
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name", "codename", "content_type__app_label"]

class MyPermissionsView(APIView):
    def get(self, request):
        return Response({
            "roles": list(request.user.roles.values("id", "name", "code")),
            "permissions": sorted(list(request.user.get_all_permissions())),
        })
