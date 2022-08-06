from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.template.response import TemplateResponse

from datetime import datetime, timedelta

from blog.models import Post, Comment


user_model = get_user_model()


class PostListView(generic.ListView):
    paginate_by = 5
    queryset = Post.objects.exclude(blocked=True)


class PostDetailView(generic.DetailView):
    queryset = Post.objects.exclude(blocked=True)


def dashboard_view(request):
    context = {
        'total_users': user_model.objects.count(),
        'total_posts': Post.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_likes': Post.objects.all().aggregate(Sum('likes')),
        'registered_per_week': user_model.objects.filter(
            created_at__gte=datetime.now()-timedelta(days=7)).count(),
    }
    return TemplateResponse(request, 'admin/dashboard.html', context)
    #return TemplateResponse(request, 'admin/index.html', context)
