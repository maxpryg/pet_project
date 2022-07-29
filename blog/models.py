from django.db import models
from django.conf import settings
from django.shortcuts import reverse

from versatileimagefield.fields import VersatileImageField, PPOIField


class Post(models.Model):
    """Model representing a post."""
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000, help_text='Enter a post text')
    likes = models.IntegerField(default=0)
    blocked = models.BooleanField(default=True)
    main_image = models.OneToOneField('MainImage', on_delete=models.CASCADE,
                                      null=True)
    additional_images = models.ManyToManyField('AdditionalImage')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this post."""
        return reverse('blog:post_detail', args=[str(self.id)])

    def short_description(self):
        return self.body[:100]

    def likes_count(self):
        return self.likes

    def comments_count(self):
        return self.comment_set.count()


class MainImage(models.Model):
    name = models.CharField('Name', max_length=100)
    image = VersatileImageField('Image', upload_to='media/images/',
                                ppoi_field='image_ppoi')
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name

    def cropped_image_url(self):
        return self.image.crop['400x400'].url

    def get_thumbnail_url(self):
        return self.image.thumbnail['100x100'].url


class AdditionalImage(models.Model):
    name = models.CharField('Name', max_length=100)
    image = VersatileImageField('Image', upload_to='media/images/',
                                ppoi_field='image_ppoi')
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name

    def cropped_image_url(self):
        return self.image.crop['300x300'].url

    def get_thumbnail_url(self):
        return self.image.thumbnail['100x100'].url


# class Image(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     name = models.CharField('Name', max_length=100)
#     is_main_image = models.BooleanField(default=False)
#     image = VersatileImageField('Image', upload_to='media/images/',
#                                 default='default.jpg')
#
# #     image = VersatileImageField('Image', upload_to='images/',
# #                                 width_field='width', height_field='height')
# #     height = models.PositiveIntegerField('Image Height', blank=True, null=True)
# #     width = models.PositiveIntegerField('Image Width', blank=True, null=True)
#
#     class Meta:
#         verbose_name = 'Image'
#         verbose_name_plural = 'Images'
#
#     def __str__(self):
#         return self.name


class Comment(models.Model):
    """Model representing a comment"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000, help_text='Enter a comment')

    def __str__(self):
        return f'{self.body}[:50]'
