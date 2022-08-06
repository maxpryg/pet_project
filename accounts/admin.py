from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from blog.models import Post
from blog.admin import admin_site


class PostInline(admin.TabularInline):
    model = Post
    extra = 1
    readonly_fields = ('title', 'short_description',)
    fields = ('title', 'short_description')

    def has_add_permission(self, request, obj):
        """Remove add button"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Remove delete button"""
        return False


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('first_name', 'last_name', 'city', 'post_count', 'blocked')
    list_filter = []
    search_fields = ('first_name', 'last_name')
    readonly_fields = ('email', 'first_name', 'last_name', 'city',
                       'birth_date', 'post_count')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'city', 'birth_date',
                           'post_count', 'blocked',)}),
    )
    actions = ['block_user']

    ordering = ('email',)

    inlines = [PostInline]

    @admin.action(description='Block user')
    def block_user(self, request, queryset):
        queryset.update(blocked=True)
        # update block field of user's posts; block posts
        queryset.get().post_set.all().update(blocked=True)


admin_site.register(CustomUser, CustomUserAdmin)
