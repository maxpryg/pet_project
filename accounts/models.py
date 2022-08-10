from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse

from .managers import CustomUserManager
from blog.models import Post


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    subscribers = models.ManyToManyField('CustomUser')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[str(self.id)])

    def post_count(self):
        return Post.objects.filter(author=self).count()
