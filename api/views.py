from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from blog.models import Post, MainImage, AdditionalImage, Subscriber
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, PostSerializer,
                             AuthorSerializer, MainImageSerializer,
                             AdditionalImageSerializer,
                             AuthorProfileSerializer, SubscriberSerializer,)


Author = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.exclude(blocked=True)
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(**{'author': user})

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        comment = CommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save(author=self.request.user, post=self.get_object())
            return Response(comment.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(comment.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = self.request.user

        if user in post.liked.all():
            return Response('This user has already liked this post',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            post.liked.add(user)
            serializer = self.get_serializer(post)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.exclude(blocked=True)
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def list(self, request, pk=None):
        queryset = Author.objects.exclude(blocked=True)
        queryset = self.filter_queryset(queryset)
        serializer = AuthorSerializer(queryset, many=True,
                                      fields=('email', 'posts'))
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Author.objects.exclude(blocked=True)
        author = get_object_or_404(queryset, pk=pk)
        serializer = AuthorSerializer(author, fields=('email',))
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subscribe(self, request, pk=None):
        author = self.get_object()
        if not self.request.user.is_authenticated:
            return Response('Unauthorized',
                            status=status.HTTP_401_UNAUTHORIZED)
        author.subscribers.add(self.request.user)
        serializer = self.get_serializer(author)
        return Response(serializer.data)


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
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AdditionalImageCreate(mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = AdditionalImage.objects.all()
    serializer_class = AdditionalImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SubscriberCreate(mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
