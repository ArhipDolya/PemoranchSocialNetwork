from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import LoginForm, RegisterForm



def homepage(request):
    return render(request, 'main_pages/homepage.html')


def registration_view(request):
    if request.method == 'GET':
        form = RegisterForm()

    return render(request, 'PemoranchApp/registration/registration.html', {'form': form})


def login_view(request):
    return render(request, 'PemoranchApp/registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')