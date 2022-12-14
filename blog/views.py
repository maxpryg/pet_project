from django.views import generic


from blog.models import Post


class PostListView(generic.ListView):
    paginate_by = 5
    queryset = Post.objects.exclude(blocked=True)


class PostDetailView(generic.DetailView):
    queryset = Post.objects.exclude(blocked=True)
