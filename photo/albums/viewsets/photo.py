from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from ..serializers import PhotoSerializer, PhotoUpdateSerializer
from ..models import Photo
from rest_framework import filters

class PhotoViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    Возвращает список Фотографий авторизованного пользователя, с дополнительной фильтрацией.
    """

    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['album', 'tags']
    search_fields = ['name', "album__name", "tags__name"]
    ordering_fields = ['created_at', 'album']
    ordering = ['album']

    def get_queryset(self):
        user = self.request.user
        items = Photo.objects.filter(user=user)
        return items


    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            if self.get_object().user == self.request.user:
                return PhotoUpdateSerializer
        elif self.action == 'create':
            return PhotoSerializer
        return PhotoSerializer


class PhotoUpdateViewSet(mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         # mixins.ListModelMixin,
                         GenericViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        items = Photo.objects.filter(user=user)
        return items


class PhotoListViewSet(mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        items = Photo.get_queryset_by_request(request=self.request, user=user)
        return items