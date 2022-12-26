from django.shortcuts import render

from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LogInForm, RegisterForm
from .models import User

# Create your views here.
def logout_user(request):
    logout(request)
    return redirect('home')

def login_user(request):
    '''
    Displays login page and logs the user in
    '''
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'account/login.html', {'error_message': "Invalid login credentials"})
    else:
        form = LogInForm()
    return render(request, 'account/login.html', {'form': form})


def register_user(request):
    '''
    Displays register page and registers user
    '''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']

            if password != password_confirm:
                return render(request, 'account/register.html', {'error_message': "Passwords do not match"})

            if User.objects.filter(username=username).exists():
                return render(request, 'account/register.html', {'error_message': "Username is already taken"})

            if User.objects.filter(email=email).exists():
                return render(request, 'account/register.html', {'error_message': "Email address is already taken"})
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'account/register.html', {'error_message': "Invalid input"})
    else:
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})