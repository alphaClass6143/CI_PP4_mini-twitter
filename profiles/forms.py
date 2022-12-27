'''
Profile forms
'''
import re
from django import forms
from django.core.validators import RegexValidator

username_regex = RegexValidator(
    re.compile('^[a-zA-Z0-9]*$'),
    'Only alphabetic and numeric characters are allowed.'
)


class SettingsForm(forms.Form):
    '''
    Settings form
    '''
    username = forms.CharField(
        max_length=30,
        validators=[username_regex],
        required=False
    )

    user_picture = forms.URLField(
        required=False
    )

    user_text = forms.CharField(
        widget=forms.Textarea,
        required=False
    )


class PasswordChangeForm(forms.Form):
    '''
    Password change form
    '''
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput
    )
