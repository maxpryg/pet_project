from django.test import TestCase

from datetime import date

from blog.models import Post
from accounts.models import CustomUser


class PostModelTest(TestCase):
    """Tests for Post model"""
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

        self.post = Post.objects.create(
            author=self.author,
            title='Post title',
            body='Post body',
        )

    def test_default_values(self):
        self.assertEquals(self.post.blocked, False)

    # TEST LABELS
    def test_author_label(self):
        post = Post.objects.get(id=self.post.id)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_title_label(self):
        post = Post.objects.get(id=self.post.id)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_body_label(self):
        post = Post.objects.get(id=self.post.id)
        field_label = post._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_blocked_label(self):
        post = Post.objects.get(id=self.post.id)
        field_label = post._meta.get_field('blocked').verbose_name
        self.assertEqual(field_label, 'blocked')

    def test_main_image_label(self):
        post = Post.objects.get(id=self.post.id)
        field_label = post._meta.get_field('main_image').verbose_name
        self.assertEqual(field_label, 'main image')
    # END TEST LABELS

    # TEST FIELD LENGTH
    def test_title_max_length(self):
        post = Post.objects.get(id=self.post.id)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_body_max_length(self):
        post = Post.objects.get(id=self.post.id)
        max_length = post._meta.get_field('body').max_length
        self.assertEqual(max_length, 10000)
    # END TEST FIELD LENGTH

    def test_object_string_representation(self):
        post = Post.objects.get(id=self.post.id)
        expected_object_string_representation = f'{post.title}'
        self.assertEqual(str(post), expected_object_string_representation)

    def test_get_absolute_url(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.get_absolute_url(), f'/{post.id}/')
