from django.test import TestCase

from datetime import date

from blog.models import Post, Comment
from accounts.models import CustomUser


class CommentModelTest(TestCase):
    """Tests for Comment model"""
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

        self.comment = Comment.objects.create(
            author=self.author,
            post=self.post,
            body='Comment body goes here...',
        )

    # TEST LABELS
    def test_author_label(self):
        comment = Comment.objects.get(id=self.comment.id)
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_post_label(self):
        comment = Comment.objects.get(id=self.comment.id)
        field_label = comment._meta.get_field('post').verbose_name
        self.assertEqual(field_label, 'post')

    def test_body_label(self):
        comment = Comment.objects.get(id=self.comment.id)
        field_label = comment._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'body')
    # END TEST LABELS

    # TEST FIELD LENGTH
    def test_body_max_length(self):
        comment = Comment.objects.get(id=self.comment.id)
        max_length = comment._meta.get_field('body').max_length
        self.assertEqual(max_length, 1000)
    # END TEST FIELD LENGTH

    def test_object_string_representation(self):
        comment = Comment.objects.get(id=self.comment.id)
        expected_object_string_representation = f'{comment.body}[:50]'
        self.assertEqual(str(comment), expected_object_string_representation)
