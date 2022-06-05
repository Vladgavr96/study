from rest_framework import serializers
from albums.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(read_only=True)
    count = serializers.IntegerField(read_only=True, source='photos.count')

    class Meta:
        model = Album
        fields = "__all__"


class AlbumFilterSerializer(serializers.Serializer):
    ordering = serializers.ListField(child=serializers.CharField(), allow_empty=True, min_length=None, max_length=None, default=[])

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass