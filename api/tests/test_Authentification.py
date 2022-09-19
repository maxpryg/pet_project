import json
from datetime import date

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user

from rest_framework import status
from rest_framework.test import APITestCase


Author = get_user_model()


class JWTTokenTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            email='test1@mail.com',
            password=make_password('password'),
            first_name='John',
            last_name='Johnson',
            city='London',
            birth_date=date.today(),
            email_verified=True
        )

    def test_anonymous_cannot_get_tokens(self):
        response = self.client.post(reverse('token_obtain_pair'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_cannot_get_refresh_tokens(self):
        response = self.client.post(reverse('token_refresh'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_can_get_tokens(self):
        response = self.client.post('/api/login/',
                                    data=json.dumps({
                                        'email': self.author.email,
                                        'password': 'password'
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)

    def test_authenticated_can_refresh_tokens(self):
        # get refresh token
        response = self.client.post('/api/login/',
                                    data=json.dumps({
                                        'email': self.author.email,
                                        'password': 'password'
                                    }),
                                    content_type='application/json')
        refresh_token = response.data.get('refresh')

        response = self.client.post('/api/token/refresh/',
                                    data=json.dumps({
                                        'refresh': refresh_token,
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
