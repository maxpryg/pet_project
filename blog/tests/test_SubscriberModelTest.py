from django.test import TestCase

from blog.models import Subscriber


class SubscriberModelTest(TestCase):
    def setUp(self):
        self.subscriber = Subscriber.objects.create(
            email='test@mail.com'
        )

    def test_object_string_representation(self):
        subscriber = Subscriber.objects.get(id=self.subscriber.id)
        expected_object_string_representation = f'{subscriber.email}'
        self.assertEqual(str(subscriber),
                         expected_object_string_representation)
