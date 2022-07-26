from django.db import models
from django.conf import settings


class Post(models.Model):
    """Model representing a post."""
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000, help_text='Enter a post text')
    likes = models.IntegerField()
    main_image = models.ImageField(upload_to ='images/main_images/')


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this blog."""
        return reverse('blog:blog_detail', args=[str(self.id)])
