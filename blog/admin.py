from django.contrib import admin

from .models import Post, Image


class ImageAdmin(admin.StackedInline):
    model = Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('fullname', 'short_description', 'likes_count',
                       'comments_count')
    list_display = ('title', 'short_description', 'fullname', 'likes_count',
                    'comments_count')
    search_fields = ('title',)
    list_filter = ('author',)
    fields = ('author', 'title', 'body', 'fullname', 'likes_count', 'comments_count')
    inlines = [ImageAdmin]

    @admin.display
    def fullname(self, obj):
        return obj.author.full_name()

    class Meta:
        model = Post


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
