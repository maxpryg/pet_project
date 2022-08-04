from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.sites.models import Site
from .tasks import send_post_creation_email

from blog.models import Post, Comment

from datetime import datetime, timedelta


user_model = get_user_model()


def dashboard_context_data():
    return {
        'total_users': user_model.objects.count(),
        'total_posts': Post.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_likes': Post.objects.all().aggregate(Sum('likes')),
        'registered_per_week': user_model.objects.filter(
            created_at__gte=datetime.now()-timedelta(days=7)).count(),
    }


def post_post_save(sender, instance, signal, *args, **kwargs):
    created = kwargs.get('created')
    if created:
        author = instance.author
        subscribers = author.subscribers.all()
        domain = Site.objects.get_current().domain
        url = f'http://{domain}{instance.get_absolute_url()}'
        for subscriber in subscribers:
            send_post_creation_email.delay(
                subscriber.id,
                f'{author.first_name} {author.last_name} created a new post.',
                f'{author.first_name} {author.last_name} created a new post. '
                f'If you want to see it, please follow the link below '
                f'{url}',)

models.signals.post_save.connect(post_post_save, sender=Post)
