from ..models import Photo
from django.contrib import admin


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
