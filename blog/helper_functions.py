from django.contrib.auth import get_user_model
from django.db.models import Sum

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
