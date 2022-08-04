import json
from datetime import date

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Post, Comment, Image
from accounts.models import CustomUser
from api.serializers import PostSerializer, CommentSerializer


class PostViewSetTest(APITestCase):
    def setUp(self):
        self.author = CustomUser.objects.create(
            email='test@mail.com',
            password='password',
            first_name='John',
            last_name='Johnson',
            city='London',
            birth_date=date.today(),
            email_verified=True
        )
        self.main_image = Image.objects.create(
            name='main_image_1',
            image='media/test_images/test_main_image.jpg')

        self.post_1 = Post.objects.create(
            author=self.author,
            title='First Post title',
            body='First Post Body',
            main_image=self.main_image,
        )

        self.post_2 = Post.objects.create(
            author=self.author,
            title='Second Post title',
            body='Second Post Body',
            main_image=self.main_image,
        )

        self.post_3 = Post.objects.create(
            author=self.author,
            title='Third Post title',
            body='Third Post Body',
            main_image=self.main_image,
        )

        self.payload = {
            'title': 'API Created Post title',
            'body': 'API Created Post Body',
            'main_image': self.main_image.id,
            'additional_images': []
        }

        self.full_payload = {
            'title': 'Full API Created Post title',
            'body': 'Full API Created Post Body',
            'main_image': self.main_image.id,
            'additional_images': []
        }

        self.partial_payload = {
            'title': 'Partial API Updated Post title',
            'body': 'Partial Updated Post Body',
        }

    def test_get_all_posts(self):
        response = self.client.get(reverse('post-list'))
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_post(self):
        response = self.client.get(
            reverse('post-detail', kwargs={'pk': self.post_1.pk}))
        post = Post.objects.get(pk=self.post_1.pk)
        serializer = PostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_post(self):
        response = self.client.get(
            reverse('post-detail', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_title_find_all(self):
        response = self.client.get(
            reverse('post-list'), {'search': 'title'})
        assert len(response.data['results']) == Post.objects.count()

    def test_search_title_find_zero(self):
        response = self.client.get(
            reverse('post-list'), {'search': 'NOTFOUND'})
        assert len(response.data['results']) == 0

    def test_search_title_find_one(self):
        response = self.client.get(
            reverse('post-list'), {'search': 'First'})
        assert len(response.data['results']) == 1

    def test_anonymous_cannot_create_post(self):
        response = self.client.post('/api/posts/',
                                    data=json.dumps(self.payload),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_create_post(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post('/api/posts/',
                                    data=json.dumps(self.payload),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_patch_post(self):
        response = self.client.patch(f'/api/posts/{self.post_1.id}/',
                                     data=json.dumps(self.partial_payload),
                                     content_type='application/json'
                                     )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_patch_post(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.patch(f'/api/posts/{self.post_1.id}/',
                                     data=json.dumps(self.partial_payload),
                                     content_type='application/json'
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_put_post(self):
        response = self.client.put(f'/api/posts/{self.post_1.id}/',
                                   data=json.dumps(self.full_payload),
                                   content_type='application/json'
                                   )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_put_post(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.put(f'/api/posts/{self.post_1.id}/',
                                   data=json.dumps(self.full_payload),
                                   content_type='application/json'
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_can_comment_post(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post(f'/api/posts/{self.post_1.id}/comment/',
                                    data=json.dumps({'body': 'comment body'}),
                                    content_type='application/json'
                                    )
        comment = Comment.objects.last()
        serializer = CommentSerializer(comment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_comment_post(self):
        response = self.client.post(f'/api/posts/{self.post_1.id}/comment/',
                                    data=json.dumps({'body': 'comment body'}),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_like_post(self):
        self.client.force_authenticate(user=self.author)
        post = Post.objects.get(id=self.post_1.id)
        post_likes_before_like = post.likes
        response = self.client.post(f'/api/posts/{self.post_1.id}/like/')
        post_likes_after_like = post.likes
        serializer = PostSerializer(post)
        self.assertEqual(post_likes_after_like, post_likes_before_like)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_like_post(self):
        response = self.client.post(f'/api/posts/{self.post_1.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
