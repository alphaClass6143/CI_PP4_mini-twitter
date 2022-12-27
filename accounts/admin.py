'''
Accounts admin page
'''
from django.contrib import admin

from accounts.models import User

# from django.contrib.auth.models import Group

# admin.site.unregister(Group)
# admin.site.unregister(Sites)

# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    '''
    User list in the admin panel
    '''
    list_filter = ['is_active']
    search_fields = ['username', 'email']
    list_display = ['username', 'email', 'is_active']
    actions = ['switch_active']

    def switch_active(self, request, queryset):
        '''
        Block user in admin panel
        '''
        queryset.update(is_active=not queryset.is_active)
