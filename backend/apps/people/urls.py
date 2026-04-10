from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, IdentityViewSet, PersonViewSet

router = DefaultRouter()
router.register("", PersonViewSet, basename="people")
router.register("contacts", ContactViewSet, basename="contacts")
router.register("identities", IdentityViewSet, basename="identities")

urlpatterns = [path("", include(router.urls))]
