from rest_framework import viewsets
from ..serializers import AlbumSerializer
from ..models import Album

from rest_framework import filters
from django.db.models import Count
from rest_framework.authtoken.models import Token

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'number_of_photos']
    ordering = ['created_at']

    def get_queryset(self):
        if self.request.META.get('HTTP_AUTHORIZATION') is not None:
            user = Token.objects.get(key=self.request.META.get('HTTP_AUTHORIZATION').split()[1]).user
        elif self.request.user:
            user = self.request.user
        queryset = Album.objects.filter(user=user)
        queryset = queryset.annotate(number_of_photos=Count('photos'))
        return queryset
