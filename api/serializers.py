from rest_framework import serializers


from blog.models import Comment, Post, AdditionalImage


class CommentSerializer(serializers.ModelSerializer):

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
