from django.shortcuts import render

from .views import Blog


def blog_detail(request, pk):
    """Blog detail view"""
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comment_set.all()

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('miniblog:blog_detail',
                                                args=[blog.id]))
    else:
        form = AddCommentForm()

    return render(request, 'miniblog/blog_detail.html',
                  context={'blog': blog, 'form': form, 'comments': comments})


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5

    class Meta:
        ordering = ['updated_at']
