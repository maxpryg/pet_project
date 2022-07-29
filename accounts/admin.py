from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from blog.models import Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 1
    readonly_fields = ('title', 'short_description',)
    fields = ('title', 'short_description')


    def has_add_permission(self, request, obj):
        return False


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('first_name', 'last_name', 'city', 'post_count')
    list_filter = []
    search_fields = ('first_name', 'last_name')
    readonly_fields = ('email', 'first_name', 'last_name', 'city',
                       'birth_date', 'post_count')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'city', 'birth_date',
                           'post_count')}),
    )

    ordering = ('email',)

    inlines = [PostInline]


admin.site.register(CustomUser, CustomUserAdmin)
