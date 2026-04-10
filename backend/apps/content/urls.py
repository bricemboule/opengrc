from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PageViewSet, PostViewSet, NewsItemViewSet

router = DefaultRouter()
router.register("pages", PageViewSet, basename="pages")
router.register("posts", PostViewSet, basename="posts")
router.register("news-items", NewsItemViewSet, basename="news-items")

urlpatterns = [path("", include(router.urls))]
