from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.sites.models import Site
from blog.tasks import send_post_creation_email

from versatileimagefield.fields import VersatileImageField, PPOIField


class Post(models.Model):
    """Model representing a post."""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000, help_text='Enter a post text')
    blocked = models.BooleanField(default=False)
    main_image = models.OneToOneField('MainImage', on_delete=models.CASCADE,
                                      null=True, blank=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this post."""
        return reverse('blog:post_detail', args=[str(self.id)])

    @property
    def short_description(self):
        return self.body[:100]

    def likes_count(self):
        return self.liked.count()

    def comments_count(self):
        return self.comment_set.count()


class Image(models.Model):
    name = models.CharField('Name', max_length=100)
    image = VersatileImageField('Image', upload_to='media/images/',
                                ppoi_field='image_ppoi')
    image_ppoi = PPOIField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def cropped_image_url(self):
        return self.image.crop['400x400'].url

    def additional_cropped_image_url(self):
        return self.image.crop['200x200'].url

    def get_thumbnail_url(self):
        return self.image.thumbnail['100x100'].url


class MainImage(Image):
    pass


class AdditionalImage(Image):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,
                             blank=True, related_name='additional_images')


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

    def __str__(self):
        return f'{self.email}'


def post_post_save(sender, instance, signal, *args, **kwargs):
    created = kwargs.get('created')
    if created:
        author = instance.author
        subscribers = author.subscribers.all()
        domain = Site.objects.get_current().domain
        url = f'{domain}{instance.get_absolute_url()}'
        for subscriber in subscribers:
            send_post_creation_email.delay(
                subscriber.id,
                f'{author.first_name} {author.last_name} created a new post.',
                f'{author.first_name} {author.last_name} created a new post. '
                f'If you want to see it, please follow the link below '
                f'{url}',)


models.signals.post_save.connect(post_post_save, sender=Post)
