from rest_framework import serializers

from django.contrib.auth import get_user_model

from versatileimagefield.serializers import VersatileImageFieldSerializer


from blog.models import Comment, Post, AdditionalImage, MainImage, Subscriber


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
            # Drop any fields that are specified in the `exclude_fields` argument.
            for field in exclude_fields:
                self.fields.pop(field)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False,
        queryset=Author.objects.all())
    post = serializers.PrimaryKeyRelatedField(required=False,
        queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'body']


class PostSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='author.first_name',
                                       read_only=True)
    last_name = serializers.CharField(source='author.last_name',
                                      read_only=True)
    main_image = serializers.PrimaryKeyRelatedField(
        queryset=MainImage.objects.all())
    additional_images = serializers.PrimaryKeyRelatedField(
        queryset=AdditionalImage.objects.all(),
        many=True,
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'first_name',
                  'last_name', 'main_image', 'additional_images']

    def to_representation(self, instance):
        """Return first 100 chars of post body"""
        representation = super().to_representation(instance)
        representation['body'] = representation['body'][:100]
        main_img_id = representation.get('main_image')
        main_img = MainImage.objects.get(id=main_img_id)
        representation['main_image'] = main_img.image.url
        return representation


class AuthorSerializer(DynamicFieldsModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(read_only=True, many=True,
                                                  source='post_set')
    class Meta:
        model = Author
        fields = ('email','first_name', 'last_name', 'birth_date', 'city',
                  'posts')


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


class SubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriber
        fields = ['email']
