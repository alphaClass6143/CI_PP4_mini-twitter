from django.contrib import admin

from .models import User

# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    '''
    User list in the admin panel
    '''
    # list_filter = ['created_on']
    search_fields = ['username']

    def block_user(self, request, queryset):
        queryset.update(blocked=True)