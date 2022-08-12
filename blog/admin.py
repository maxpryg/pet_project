from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.urls import path
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.template.response import TemplateResponse
from django.utils import timezone

from datetime import timedelta

from .models import Post, Comment, AdditionalImage


user_model = get_user_model()


class DashboardAdminSite(AdminSite):
    index_template = "admin/custom_index.html"

    def dashboard_view(self, request):
        context = {
            'total_users': user_model.objects.count(),
            'total_posts': Post.objects.count(),
            'total_comments': Comment.objects.count(),
            'total_likes': Post.objects.all().aggregate(Sum('likes')),
            'registered_per_week': user_model.objects.filter(
                date_joined=timezone.now()-timedelta(days=7)).count(),
        }
        return TemplateResponse(request, 'admin/dashboard.html', context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view),
                 name='dashboard_view')
        ]
        return my_urls + urls


admin_site = DashboardAdminSite(name='pet_project_admin')


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('short_description', 'likes_count', 'comments_count',
                       'author_full_name')
    list_display = ('title', 'short_description', 'author_full_name',
                    'likes_count', 'comments_count', 'blocked')
    search_fields = ('title',)
    list_filter = ('author',)
    fields = ('author', 'title', 'body', 'main_image', 'likes_count',
              'comments_count', 'blocked')
    actions = ['block_post']
    inlines = [AdditionalImageInline]

    @admin.display
    def author_full_name(self, obj):
        return obj.author.get_full_name()

    @admin.action(description='Block post')
    def block_post(self, request, queryset):
        queryset.update(blocked=True)

    class Meta:
        model = Post


admin_site.register(Post, PostAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
