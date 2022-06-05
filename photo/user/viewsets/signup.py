from rest_framework import viewsets, mixins

from user.serializers import UserSerializer
from user.models import User


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer