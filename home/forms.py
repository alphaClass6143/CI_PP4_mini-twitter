from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

class LogInForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)