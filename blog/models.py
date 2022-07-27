from django.db import models
from django.conf import settings
from django.shortcuts import reverse

from versatileimagefield.fields import VersatileImageField


class Post(models.Model):
    """Model representing a post."""
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000, help_text='Enter a post text')
    likes = models.IntegerField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this blog."""
        return reverse('blog:blog_detail', args=[str(self.id)])


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=100)
    is_main_image = models.BooleanField(default=False)
    image = VersatileImageField('Image', upload_to='images/',
                                width_field='width', height_field='height')
    height = models.PositiveIntegerField('Image Height', blank=True, null=True)
    width = models.PositiveIntegerField('Image Width', blank=True, null=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Model representing a comment"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000, help_text='Enter a comment')

    def __str__(self):
        return f'{self.body}[:50]'
