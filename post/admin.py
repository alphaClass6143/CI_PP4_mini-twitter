from django.contrib import admin

from .models import Post, PostComment

# Register your models here.
@admin.register(Post)
class Post(admin.ModelAdmin):
    '''
    Post list in the admin panel
    '''
    list_filter = ['created_at']
    search_fields = ['created_at', 'content']
    list_display = ['get_username', 'content', 'created_at']


@admin.register(PostComment)
class PostComment(admin.ModelAdmin):
    '''
    PostComment list in the admin panel
    '''
    list_display = ('content', 'created_at')
    list_filter = ('post', 'created_at')
    search_fields = ['content']