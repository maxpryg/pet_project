from rest_framework import serializers

from django.contrib.auth import get_user_model

from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_flex_fields.serializers import FlexFieldsModelSerializer


from blog.models import Comment, Post, AdditionalImage, MainImage


Author = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    #author = serializers.ReadOnlyField(source='author.id')
    #post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'body']


class PostSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='author.first_name',
                                       read_only=True)
    last_name = serializers.CharField(source='author.last_name',
                                      read_only=True)
    main_image = serializers.CharField(source='main_image.image.url')
    additional_images = serializers.PrimaryKeyRelatedField(
        queryset=AdditionalImage.objects.all(),
        many=True,
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'short_description', 'first_name',
                  'last_name', 'main_image', 'additional_images']

    def create(self, validated_data):
        #print('vdata:', validated_data.pop('additional_images'))
        additional_images =  validated_data.pop('additional_images')
        post =  Post.objects.create(**validated_data)
        #AdditionalImage.objects.create(post=post, **additional_images)
        return post


class AuthorSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(read_only=True, many=True,
                                                  source='post_set')

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'birth_date', 'city', 'posts')


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('email', 'first_name', 'last_name', 'birth_date', 'city')


class MainImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = MainImage
        fields = ['id', 'name', 'image']


class AdditionalImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = AdditionalImage
        fields = ['id', 'name', 'image']
