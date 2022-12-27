'''
Forms for the accounts app
'''
import re

from django import forms
from django.core.validators import RegexValidator

# Regex checking for the correct username
username_regex = RegexValidator(
    re.compile('^[a-zA-Z0-9]*$'),
    'Only alphabetic and numeric characters are allowed.'
)


class RegisterForm(forms.Form):
    '''
    Register form
    '''
    username = forms.CharField(
        max_length=30,
        validators=[username_regex]
    )

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput
    )


class LogInForm(forms.Form):
    '''
    Login form
    '''
    email = forms.CharField(
        max_length=50
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )
