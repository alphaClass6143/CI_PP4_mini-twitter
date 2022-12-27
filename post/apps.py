'''
app config for post app
'''
from django.apps import AppConfig


class PostConfig(AppConfig):
    '''
    PostConfig
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post'
