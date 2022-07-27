from django.urls import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Post
#from .forms import AddCommentForm


# def post_detail(request, pk):
#     """Post detail view"""
#     post = get_object_or_404(Post, pk=pk)
#     comments = post.comment_set.all()
#
#     if request.method == 'POST':
#         form = AddCommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#             return HttpResponseRedirect(reverse('blog:post_detail',
#                                                 args=[post.id]))
#     else:
#         form = AddCommentForm()
#
#     return render(request, 'blog/post_detail.html',
#                   context={'post': post, 'form': form, 'comments': comments})


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = Post
