'''
Views for the accounts app
'''
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate

from accounts.forms import LogInForm, RegisterForm
from accounts.models import User


# Create your views here.
def logout_user(request):
    '''
    Logs the user out
    '''
    logout(request)
    return redirect('home')


def login_user(request):
    '''
    Displays login page and logs the user in
    '''
    #
    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            # Login successful
            if user is not None:
                login(request, user)
                return redirect('home')

            # Login failed - invalid credentials
            return render(request,
                          'account/login.html',
                          {'error_message': "Invalid login credentials"})

        # Login failed - request was incorrect (form error)
        return render(request,
                      'account/login.html',
                      {'error_message': "Invalid request"})

    # Render login
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

            # Register failed - passwords do not match
            if password != password_confirm:
                return render(request,
                              'account/register.html',
                              {'error_message': "Passwords do not match"})

            # Register failed - username is taken
            if User.objects.filter(username=username).exists():
                return render(request,
                              'account/register.html',
                              {'error_message': "Username is already taken"})

            # Register failed - email already exists
            if User.objects.filter(email=email).exists():
                return render(request,
                              'account/register.html',
                              {'error_message': "Email address is already taken"})

            # Create user
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()

            # Login in user and redirect to home
            login(request, user)
            return redirect('home')

        # Register failed - invalid input (form error)
        return render(request, 'account/register.html',
                      {'error_message': "Invalid input"})

    # Render register form
    form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})
