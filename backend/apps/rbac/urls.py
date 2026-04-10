from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PermissionListView, MyPermissionsView

router = DefaultRouter()
router.register("roles", RoleViewSet, basename="roles")

urlpatterns = [
    path("", include(router.urls)),
    path("permissions/", PermissionListView.as_view(), name="permissions"),
    path("my-permissions/", MyPermissionsView.as_view(), name="my-permissions"),
]
