from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..serializers import AlbumSerializer
from ..models import Album

# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'count']
    ordering = ['created_at']

    def get_queryset(self):
        user = self.request.user
        # print(user)
        items = Album.objects.filter(user=user)
        return items