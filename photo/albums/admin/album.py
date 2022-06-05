from ..models import Album
from django.contrib import admin


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass
