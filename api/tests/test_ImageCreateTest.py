# from datetime import date
#
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from blog.models import Image
# from accounts.models import CustomUser
#
#
# class ImageCreateTest(APITestCase):
#     def setUp(self):
#         self.author_1 = CustomUser.objects.create(
#             email='test@mail.com',
#             password='password',
#             first_name='John',
#             last_name='Johnson',
#             city='London',
#             birth_date=date.today(),
#             email_verified=True
#         )
#
# #         self.image = Image.objects.create(name='test_image',
# #                                           image='testimage.jpg')
#         self.image = VersatileImageField('Image', upload_to='media/test_images/',
#                                 ppoi_field='image_ppoi')
#
#     def test_upload_image(self):
#         self.client.force_authenticate(user=self.author_1)
#         response = self.client.post('/api/image/',
#                                     data={
#                                         'name': 'testimage',
#                                         'image': 'imagedir/'},
#                                     format='multipart'
#                                     )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
