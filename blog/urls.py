from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    #path('<int:pk>/', views.blog_detail, name='blog_detail'),
#     path('authors/', views.AuthorListView.as_view(), name='authors'),
#     path('author/<int:pk>', views.AuthorDetailView.as_view(),
#          name='author_detail'),
#     path('author/<int:pk>/profile', views.author_profile,
#          name='author_profile'),
]
