from django.views import generic


from blog.models import Post, Comment


class PostListView(generic.ListView):
    paginate_by = 5
    queryset = Post.objects.exclude(blocked=True)


class PostDetailView(generic.DetailView):
    queryset = Post.objects.exclude(blocked=True)


#def dashboard_view(request):
#    data = {
#        'total_users': user_model.objects.count(),
#        'total_posts': Post.objects.count(),
#        'total_comments': Comment.objects.count(),
#        'total_likes': Post.objects.all().aggregate(Sum('likes')),
#        'registered_per_week': user_model.objects.filter(
#            created_at__gte=datetime.now()-timedelta(days=7)).count(),
#    }
#    #return TemplateResponse(request, 'admin/dashboard.html', context)
#    #return TemplateResponse(request, 'admin/index.html', {'data': data})
#    return TemplateResponse(request, 'admin/dashboard.html', {'data': data})
