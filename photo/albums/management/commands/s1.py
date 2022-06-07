from django.core.management.base import BaseCommand
from albums.models import Tag, Album, Photo
from user.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        Tag.objects.create(name='start_tag1')
        Tag.objects.create(name='start_tag2')
        user1 = User.objects.create(username='test_user', password='Qdf1337ak', email='email1@mail.ru',
                            is_active=True)
        user2 = User.objects.create(username='test_user2', password='Qdf0075ak', email='email1@mail.ru',
                            is_active=True)
        a1 = Album.objects.create(name='First Album', user=user1)
        a2 = Album.objects.create(name='Second Album', user=user2)
        t1 = Tag.objects.create(name='tag1')
        t2 = Tag.objects.create(name='tag2')
        Photo.objects.create(name='photo1', photo='test/img1.jpg', album=a1, user=user1).tags.set([])
        Photo.objects.create(name='photo2', photo='test/img2.jpg', album=a1, user=user1).tags.set(
            [t1, t2])
        Photo.objects.create(name='photo3', photo='test/img3.jpeg', album=a2, user=user2).tags.set([])
        Photo.objects.create(name='photo4', photo='test/img4.jpeg', album=a2, user=user2).tags.set([t1])