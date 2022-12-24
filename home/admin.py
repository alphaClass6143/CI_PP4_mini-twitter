from django.contrib import admin
from .models import Post, PostComment, Profile

# Register your models here.
@admin.register(Post)
class Post(admin.ModelAdmin):
    list_filter = ['created_on']
    search_fields = ['created_on', 'content']
    # list_display = ('title', 'slug', 'status', 'created_on')


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    # list_filter = ['created_on']
    search_fields = ['username']

    def block_user(self, request, queryset):
        queryset.update(blocked=True)


@admin.register(PostComment)
class PostComment(admin.ModelAdmin):
    list_display = ('content', 'created_on')
    list_filter = ('post', 'created_on')
    search_fields = ['content']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

