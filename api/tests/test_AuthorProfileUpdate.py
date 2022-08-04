import json
from datetime import date

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import AuthorProfileSerializer


Author = get_user_model()


class AuthorProfileUpdateTest(APITestCase):
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

        self.full_payload = {
            'email': 'newtest2@mail.com',
            'first_name': 'NewBen',
            'last_name': 'NewBenson',
            'city': 'NewLondon',
            'birth_date': date.today(),
        }

        self.partial_payload = {
            'first_name': 'NewBen',
            'last_name': 'NewBenson',
            'city': 'NewLondon',
        }

    def test_anonymous_cannot_get_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_can_get_profile(self):
        self.client.force_authenticate(user=self.author_1)
        response = self.client.get(reverse('profile'))
        serializer = AuthorProfileSerializer(self.author_1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_patch_profile(self):
        response = self.client.patch('/api/profile/',
                                     data=json.dumps(self.partial_payload),
                                     content_type='application/json'
                                     )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_can_patch_profile(self):
        self.client.force_authenticate(user=self.author_1)
        response = self.client.patch('/api/profile/',
                                     data=json.dumps(self.partial_payload),
                                     content_type='application/json'
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_can_put_profile(self):
        self.client.force_authenticate(user=self.author_1)
        response = self.client.put('/api/profile/',
                                   data=json.dumps(self.full_payload,
                                                   default=str),
                                   content_type='application/json'
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_put_profile(self):
        response = self.client.patch('/api/profile/',
                                     data=json.dumps(self.full_payload,
                                     default=str),
                                     content_type='application/json'
                                     )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
