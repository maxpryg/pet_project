from django.contrib import admin
from django.contrib.sites.models import Site

from .models import Post, Image


admin.site.unregister(Site)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('fullname', 'short_description', 'likes_count',
                       'comments_count')
    list_display = ('title', 'short_description', 'fullname', 'likes_count',
                    'comments_count', 'blocked')
    search_fields = ('title',)
    list_filter = ('author',)
    fields = ('author', 'title', 'body', 'main_image', 'additional_images',
              'fullname', 'likes_count', 'comments_count', 'blocked')
    actions = ['block_post']

    @admin.display
    def fullname(self, obj):
        return obj.author.full_name()

    @admin.action(description='Block post')
    def block_post(self, request, queryset):
        queryset.update(blocked=True)

    class Meta:
        model = Post


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
