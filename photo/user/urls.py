from rest_framework import routers
from user.viewsets import UserViewSet, GetTokenViewSet

# from django.urls import path, include


urlpatterns = [

]

router = routers.DefaultRouter()
router.register('signup', UserViewSet)
router.register('gettoken_to_curent_user', GetTokenViewSet, basename='token')
urlpatterns += router.urls
