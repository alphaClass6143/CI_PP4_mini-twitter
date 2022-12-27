'''
Forms for the post app
'''
from django import forms


class PostForm(forms.Form):
    '''
    Post form
    '''
    content = forms.CharField(
        widget=forms.Textarea
    )


class CommentForm(forms.Form):
    '''
    Comment form
    '''
    content = forms.CharField(
        widget=forms.Textarea
    )
