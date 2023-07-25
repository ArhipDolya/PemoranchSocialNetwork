from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout


def homepage(request):
    return render(request, 'PemoranchApp/homepage.html')



def registration_view(request):
    return render(request, 'PemoranchApp/registration/registration.html')


def login_view(request):
    return render(request, 'PemoranchApp/registration/login.html')


def logout_view(request):
    #return render(request, 'PemoranchApp/registration/logout.html')
    logout(request)
    return redirect('homepage')