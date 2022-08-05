from django.contrib import admin
from django.contrib.sites.models import Site
from django.urls import path

from .models import Post
from blog.views import dashboard_view


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

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('dashboard/', self.admin_site.admin_view(dashboard_view))
        ]
        return my_urls + urls

    class Meta:
        model = Post
