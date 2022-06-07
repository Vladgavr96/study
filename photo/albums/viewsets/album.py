from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..serializers import AlbumSerializer
from ..models import Album

from rest_framework import filters
from django.db.models import Count

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'number_of_photos']
    ordering = ['created_at']

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        queryset = queryset.annotate(number_of_photos=Count('photos'))
        return queryset