from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters

#from django_filters import rest_framework as filters

from blog.models import Comment, Post, MainImage
from api.serializers import CommentSerializer, PostSerializer


# class ProductFilter(filters.FilterSet):
#     author = filters.CharFilter(lookup_expr='icontains',
#                                 field_name='author__first_name')
#     author = filters.CharFilter(lookup_expr='icontains',
#                                 field_name='author__last_name')
#
#     class Meta:
#         model = Post
#         fields = ['author']


class CommentCreate(mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostViewSet(generics.ListCreateAPIView,
                  mixins.UpdateModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['author__first_name', 'author__last_name', 'author']
    search_fields = ['title']

    def perform_create(self, serializer):
        user = self.request.user
        main_image_id = self.request.data.get('main_image')
        main_image = MainImage.objects.get(id=main_image_id)
        serializer.save(**{'author': user,
                           'main_image': main_image
                           })
