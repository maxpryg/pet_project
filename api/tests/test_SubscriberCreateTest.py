import json

from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Subscriber


class SubscriberCreateTest(APITestCase):
    def setUp(self):
        self.correct_email = 'test@mail.com'
        self.incorrect_email = 'testmail.com'

    def test_anonymous_can_subscribe_with_correct_email(self):
        assert self.correct_email not in Subscriber.objects.values_list(
            'email', flat=True)
        response = self.client.post('/api/subscribe/',
                                    data=json.dumps(
                                        {'email': self.correct_email}),
                                    content_type='application/json'
                                    )
        assert self.correct_email in Subscriber.objects.values_list(
            'email', flat=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_subscribe_with_incorrect_email(self):
        assert self.incorrect_email not in Subscriber.objects.values_list(
            'email', flat=True)
        response = self.client.post('/api/subscribe/',
                                    data=json.dumps(
                                        {'email': self.incorrect_email}),
                                    content_type='application/json'
                                    )
        assert self.correct_email not in Subscriber.objects.values_list(
            'email', flat=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
