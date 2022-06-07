from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import TestCase, Client
from albums.models import Album, Tag, Photo
from django.contrib.auth.hashers import make_password
import json
from user.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class AlbumTestCase(APITestCase):

    def setUp(self):
        self.register_url = '/api/v1/user/signup/'
        self.login_url = '/api/v1/api-auth/login/'
        self.album_list_url = '/api/v1/albums/'

        u1 = User.objects.create(username='User1', password=make_password('password1'), email='email1@mail.ru',
                                 is_active=True)
        u2 = User.objects.create(username='User2', password=make_password('password2'), email='email2@mail.ru',
                                 is_active=True)
        User.objects.create(username='User3', password=make_password('password3'), email='email3@mail.ru',
                            is_active=True)

        a1 = Album.objects.create(name='Album1.1', user=u1)
        a2 = Album.objects.create(name='Album1.2', user=u1)
        Album.objects.create(name='Album1.3', user=u1)
        a3 = Album.objects.create(name='Album2.1', user=u2)
        t1 = Tag.objects.create(name='tag1')
        t2 = Tag.objects.create(name='tag2')
        Photo.objects.create(name='photo1', photo='test/img1.jpg', album=a1, user=u1).tags.set([])
        Photo.objects.create(name='photo2', photo='test/img2.jpg', album=a1, user=u1).tags.set(
            [t1, t2])
        Photo.objects.create(name='photo3', photo='test/img3.jpeg', album=a2, user=u1).tags.set([])
        Photo.objects.create(name='photo4', photo='test/img4.jpeg', album=a3, user=u2).tags.set([t1])

    def test_unauthorized_album(self):
        # проверка на доступ к альбомам не авторизованного пользователя
        client = Client()
        response = client.get('/api/v1/albums/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_photos(self):
        # проверка на доступ к фото не авторизованного пользователя
        client = Client()
        response = client.get('/api/v1/photos/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_album_1(self):
        albums_number = len(Album.objects.all())
        u1 = User.objects.get(username='User1')
        Album.objects.create(name='Album', user=u1)
        self.assertEqual(len(Album.objects.all()), albums_number + 1)

    def test_user_login_2(self):
        c = Client()
        response = c.post(self.login_url, {'username': 'User1', 'password': 'password1'})
        self.assertEqual(response.status_code, 302)

    def test_get_albums_api_status_3(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/albums/')
        self.assertEqual(response.status_code, 200)

    def test_get_albums_api_context_4(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/albums/')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 3)
        names = [album['name'] for album in content]
        self.assertTrue("Album1.3" in names)

    def test_post_albums_api_5(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.post('/api/v1/albums/', {'name': 'Album1.4'})
        self.assertEqual(response.status_code, 201)

    def test_get_album_api_6(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/albums/')
        content = json.loads(response.content.decode('utf-8'))
        ids = [album['id'] for album in content]
        album_id = ids[0]
        response = c.get(f'/api/v1/albums/{album_id}/')
        self.assertEqual(response.status_code, 200)

    def test_put_album_api_7(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/albums/')
        content = json.loads(response.content.decode('utf-8'))
        ids = [album['id'] for album in content]
        album_id = ids[0]
        c.put(f'/api/v1/albums/{album_id}/', {'name': 'Album1.4'}, content_type='application/json')
        response = c.get(f'/api/v1/albums/{album_id}/')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['name'], 'Album1.4')

    def test_delete_album_api_8(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/albums/')
        content = json.loads(response.content.decode('utf-8'))
        ids = [album['id'] for album in content]
        album_id = ids[0]
        c.delete(f'/api/v1/albums/{album_id}/')
        response = c.get(f'/api/v1/albums/{album_id}/')
        self.assertEqual(response.status_code, 404)

    def test_get_photos_api_status_9(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/photos/')
        self.assertEqual(response.status_code, 200)

    def test_get_photos_api_context_10(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/photos/')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 3)
        titles = [photo['name'] for photo in content]
        self.assertTrue("photo3" in titles)

    def test_create_photos_base_11(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_path = dir_path + '/img5.jpeg'
        tag3 = Tag.objects.create(name='tag3')
        image = SimpleUploadedFile(name='img5.jpeg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        album = Album.objects.filter(name='Album1.1').get()
        Photo.objects.create(name='photo5', photo=image, album=album).tags.set([tag3])
        self.assertEqual(len(Photo.objects.all()), 5)

    def test_get_photo_api_12(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/photos/')
        content = json.loads(response.content.decode('utf-8'))
        ids = [photo['id'] for photo in content]
        photo_id = ids[0]
        response = c.get(f'/api/v1/photos/{photo_id}/')
        self.assertEqual(response.status_code, 200)

    def test_patch_photo_api_13(self):
        c = Client()
        c.login(username='User1', password='password1')
        response = c.get('/api/v1/photos/')
        content = json.loads(response.content.decode('utf-8'))
        ids = [photo['id'] for photo in content]
        photo_id = ids[0]
        c.patch(f'/api/v1/photos/{photo_id}/', {'name': 'updated_photo'}, content_type='application/json')
        response = c.get(f'/api/v1/photos/{photo_id}/')
        content = json.loads(response.content.decode('utf-8'))
        print(content)
        self.assertEqual(content['name'], 'updated_photo')
