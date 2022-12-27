'''
Post urls
'''
from django.urls import path, include
from post import views


urlpatterns = [
    path('new_post/', views.new_post, name='new_post'),
    path('post/<int:post_id>', views.view_post, name='view_post'),
    path('post/<int:post_id>/vote/<int:vote_type>',
         views.vote_post,
         name='vote_post'),
    path('post/<int:post_id>/add_comment',
         views.add_comment,
         name='add_comment'),
    path('comment/<int:comment_id>/edit',
         views.edit_comment,
         name='edit_comment'),
    path('comment/<int:comment_id>/delete',
         views.delete_comment,
         name='delete_comment'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]