from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, JobTitleViewSet, StaffViewSet

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="departments")
router.register("job-titles", JobTitleViewSet, basename="job-titles")
router.register("staffs", StaffViewSet, basename="staffs")

urlpatterns = [path("", include(router.urls))]
