from django.test import TestCase
from django.urls import reverse

from datetime import date

from blog.models import Post
from accounts.models import CustomUser


class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = CustomUser.objects.create(
            email='test@mail.com',
            password='password',
            first_name='John',
            last_name='Johnson',
            city='London',
            birth_date=date.today(),
            email_verified=True
        )

        # Create 13 posts for pagination tests
        number_of_posts = 13
        for post_id in range(number_of_posts):
            Post.objects.create(
                author=author,
                title='Post title {post_id}',
                body='Post body {post_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'], True)
        self.assertEqual(len(response.context['post_list']), 5)

    def test_lists_all_posts(self):
        # Get third page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('blog:post_list')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'], True)
        self.assertEqual(len(response.context['post_list']), 3)


class PostDetailViewTest(TestCase):
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blog:post_detail',
                                           kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blog:post_detail',
                                           kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
