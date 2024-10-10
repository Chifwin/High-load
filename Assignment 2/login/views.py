from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from login.forms import UserForm
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def user_new(request: HttpResponse):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.AFTER_LOGIN_URL)
        error = "Invalid credentials!"
    return render(request, 'login.html', {'form': UserForm(), 'error': error, 'page_name': 'New user'})


def user_login(request: HttpResponse):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.AFTER_LOGIN_URL)
        error = "Invalid credentials!"
    return render(request, 'login.html', {'form': UserForm(), 'error': error, 'page_name': 'Login'})


def user_logout(request: HttpResponse):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
