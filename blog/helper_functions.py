from django.contrib.auth import get_user_model

from blog.models import Post, Comment


user_model = get_user_model()


def dashboard_context_data():
    return {
        'total_users': user_model.objects.count(),
        'total_posts': Post.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_likes': Post.objects.all().aggregate(Sum('likes')),
        #'registered_per_week': user_model.registered_per_week(),
    }
