from django.contrib import admin

from .models import Post, MainImage, AdditionalImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('fullname', 'short_description', 'likes_count',
                       'comments_count')
    list_display = ('title', 'short_description', 'fullname', 'likes_count',
                    'comments_count')
    search_fields = ('title',)
    list_filter = ('author',)
    fields = ('author', 'title', 'body', 'main_image', 'additional_images',
              'fullname', 'likes_count', 'comments_count')

    @admin.display
    def fullname(self, obj):
        return obj.author.full_name()

    class Meta:
        model = Post


@admin.register(MainImage)
class MainImageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(AdditionalImage)
class AdditionalImageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
