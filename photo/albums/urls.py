from rest_framework.routers import DefaultRouter

from .viewsets import AlbumViewSet, PhotoViewSet

router = DefaultRouter()

router.register(r'albums', AlbumViewSet)
router.register(r'photos', PhotoViewSet)

urlpatterns = router.urls