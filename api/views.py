from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from blog.models import Comment, Post, MainImage, AdditionalImage
from api.serializers import (CommentSerializer,
                             PostSerializer,
                             AuthorSerializer,
                             MainImageSerializer,
                             AdditionalImageSerializer,
                             AuthorProfileSerializer
                             )


Author = get_user_model()


class CommentCreate(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

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


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']


class AuthorProfileUpdate(generics.RetrieveUpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorProfileSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class MainImageCreate(mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = MainImage.objects.all()
    serializer_class = MainImageSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AdditionalImageCreate(mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = AdditionalImage.objects.all()
    serializer_class = AdditionalImageSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
