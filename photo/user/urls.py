from rest_framework import routers
from user.viewsets.signup import UserViewSet

router = routers.DefaultRouter()
router.register('signup', UserViewSet)
urlpatterns = router.urls
