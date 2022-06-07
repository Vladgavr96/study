from django.db import models
from django.http import HttpRequest
from ..models.tag import Tag
from ..models.album import Album
from django.core.validators import FileExtensionValidator
import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from user.models import User
from django.utils import timezone

extensions = [
    'jpg',
    'jpeg',
    'png',
]


def validate_image_size(image_field_obj):
    file_size = image_field_obj.size
    megabyte_limit = 5.0
    if file_size > megabyte_limit * 1024 * 1024:
        from django.core.exceptions import ValidationError
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def validate_image_content_type(image_field_obj):
    allowed_types = [
        'image/jpeg',
        'image/png',
    ]

    file = image_field_obj

    from django.db.models.fields.files import ImageFieldFile
    from django.core.exceptions import ValidationError
    from django.core.files.uploadedfile import InMemoryUploadedFile

    if isinstance(file, ImageFieldFile):
        file = file.file

    if not isinstance(file, InMemoryUploadedFile):
        return

    try:
        content_type = file.content_type
    except Exception:
        raise ValidationError(
            f'Не удалось определить MIME тип файла. Разрешенные MIME  типы: {", ".join(allowed_types)}.', )

    if not (content_type in allowed_types):
        raise ValidationError(
            f'MIME  тип  файла “{content_type}” не допускается. Разрешенные MIME  типы: {", ".join(allowed_types)}.',
        )


class Photo(models.Model):
    name = models.CharField(verbose_name="Название", max_length=256, unique=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', default=timezone.now)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE, related_name='photos', null=False)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name="photos", blank=True)
    photo = models.ImageField(verbose_name="Изображение", blank=False, null=False, upload_to='photos',
                              validators=[validate_image_size, validate_image_content_type,
                                          FileExtensionValidator(allowed_extensions=extensions), ])
    thumbnail = models.ImageField(upload_to='thumbs', editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo', verbose_name='Пользователь',
                             null=True)

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Photo, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def make_thumbnail(self):
        THUMB_SIZE = (100, 200)

        image = Image.open(self.photo)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


