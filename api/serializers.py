from rest_framework import serializers

from django.contrib.auth import get_user_model

from versatileimagefield.serializers import VersatileImageFieldSerializer


from blog.models import Comment, Post, MainImage, AdditionalImage, Subscriber


Author = get_user_model()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be excluded.
    """
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        exclude_fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if exclude_fields is not None:
            # Drop any fields that are specified in the `exclude_fields`
            # argument.
            for field in exclude_fields:
                self.fields.pop(field)


class AuthorSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Author
        fields = ('email', 'first_name', 'last_name', 'birth_date', 'city',
                  'posts')


class AuthorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('email', 'first_name', 'last_name', 'birth_date', 'city')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False,
                                                queryset=Author.objects.all())
    post = serializers.PrimaryKeyRelatedField(required=False,
                                              queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'body']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(fields=('email', 'birth_date', 'city', 'posts'),
                              required=False)
    main_image_url = serializers.URLField(source='main_image.image.url',
                                          read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'short_description', 'author',
                  'main_image_url', 'main_image']

        extra_kwargs = {'body': {'write_only': True},
                        'main_image': {'write_only': True}}


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


class SubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriber
        fields = ['email']
