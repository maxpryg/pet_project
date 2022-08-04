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
    blocked = models.BooleanField(default=False)
    main_image = models.ForeignKey('Image', on_delete=models.CASCADE,
                                   related_name='main_image',
                                   null=True)
    additional_images = models.ManyToManyField('Image',
                                               blank=True,
                                               related_name='additional_images'
                                               )

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


class Image(models.Model):
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


class Comment(models.Model):
    """Model representing a comment"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000, help_text='Enter a comment')

    def __str__(self):
        return f'{self.body}[:50]'


class Subscriber(models.Model):
    """Model representing a subscriber"""
    email = models.EmailField('email address', unique=True)
