from django.contrib import admin

from .models import Post, Image


class ImageAdmin(admin.StackedInline):
    model = Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]

    class Meta:
        model = Post


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
