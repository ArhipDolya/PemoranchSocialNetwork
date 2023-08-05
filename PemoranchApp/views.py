from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

from .forms import LoginForm, RegisterForm



def homepage(request):
    return render(request, 'main_pages/homepage.html')


def registration_view(request):
    if request.method == 'GET':
        form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You registered successfully!')
            login(request, user)
            return redirect("/")

    return render(request, 'PemoranchApp/registration/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('password', 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'PemoranchApp/registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('homepage')