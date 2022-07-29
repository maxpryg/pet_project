from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse

from .managers import CustomUserManager
from blog.models import Post
from django.utils import timezone


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    #birth_date = models.DateField(default=timezone.now())
    birth_date = models.DateField()
    email_verified = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[str(self.id)])
        pass

    def post_count(self):
        return Post.objects.filter(author=self).count()


class Dashboard(CustomUser):
    pass
