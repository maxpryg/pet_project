from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import now

from .managers import CustomUserManager
from blog.models import Post


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    birth_date = models.DateField()
    email_verified = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    subscribers = models.ManyToManyField('CustomUser')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[str(self.id)])

    def post_count(self):
        return Post.objects.filter(author=self).count()
