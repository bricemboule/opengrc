from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet

from .models import User
from .serializers import LoginSerializer, UserSerializer, build_login_payload


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(build_login_payload(user), status=status.HTTP_200_OK)


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class LogoutView(APIView):
    def post(self, request):
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class UserViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = User.objects.select_related("organization").prefetch_related("roles").all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["email", "username", "full_name", "phone"]
    ordering_fields = ["id", "email", "full_name", "created_at"]
