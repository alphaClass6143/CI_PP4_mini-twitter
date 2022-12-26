from django import forms
import re
from django.core.validators import RegexValidator


class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)