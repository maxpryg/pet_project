from datetime import date

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


from api.serializers import AuthorSerializer


Author = get_user_model()


class AuthorViewSetTest(APITestCase):
    def setUp(self):
        self.author_1 = Author.objects.create(
            email='test1@mail.com',
            password='password',
            first_name='John',
            last_name='Johnson',
            city='London',
            birth_date=date.today(),
            email_verified=True
        )

        self.author_2 = Author.objects.create(
            email='test2@mail.com',
            password='password',
            first_name='Ben',
            last_name='Benson',
            city='London',
            birth_date=date.today(),
            email_verified=True
        )

        self.author_3 = Author.objects.create(
            email='test3@mail.com',
            password='password',
            first_name='Jack',
            last_name='Jackson',
            city='London',
            birth_date=date.today(),
            email_verified=True
        )

    def test_get_all_authors(self):
        response = self.client.get(reverse('authors-list'))
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True,
                                      fields=('email', 'posts'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_singel_authors(self):
        response = self.client.get(reverse('authors-detail',
                                           kwargs={'pk': self.author_1.id}))
        author = Author.objects.get(pk=self.author_1.id)
        serializer = AuthorSerializer(author, fields=('email',))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_singel_authors(self):
        response = self.client.get(reverse('authors-detail',
                                           kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_first_name_find_one(self):
        response = self.client.get(
            reverse('authors-list'), {'search': 'John'})
        self.assertEqual(len(response.data), 1)

    def test_search_last_name_find_zero(self):
        response = self.client.get(
            reverse('authors-list'), {'search': 'NOTFOUND'})
        self.assertEqual(len(response.data), 0)

    def test_authenticated_can_subscribe_to_author(self):
        subscriber = self.author_1
        self.client.force_authenticate(user=subscriber)
        self.assertNotIn(subscriber, self.author_2.subscribers.all())

        response = self.client.get(
            f'/api/authors/{self.author_2.id}/subscribe/')
        self.assertIn(subscriber, self.author_2.subscribers.all())

        serializer = AuthorSerializer(self.author_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_anonymous_cannot_subscribe_to_author(self):
        response = self.client.get(
            f'/api/authors/{self.author_2.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
