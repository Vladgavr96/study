from rest_framework import serializers

from albums.models import Photo, Album


class AlbumsPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Album.objects.filter(user=user)
        return queryset


class ImageInfoSerializer(serializers.Serializer):
    url = serializers.CharField(read_only=True)
    width = serializers.IntegerField(read_only=True)
    height = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PhotoSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_info = ImageInfoSerializer(read_only=True, source="image", )
    image_small_info = ImageInfoSerializer(read_only=True, source="image_small", )
    album = AlbumsPKField()

    class Meta:
        model = Photo
        exclude = ("updated_at",)
        read_only_fields = ['image_small']


class PhotoUpdateSerializer(PhotoSerializer):
    class Meta(PhotoSerializer.Meta):
        read_only_fields = ['image_small', "image"]
