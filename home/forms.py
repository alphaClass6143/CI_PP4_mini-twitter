'''
Home forms
'''
from django import forms


class PostForm(forms.Form):
    '''
    Post form
    '''
    content = forms.CharField(widget=forms.Textarea)
