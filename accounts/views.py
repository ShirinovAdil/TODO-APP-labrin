from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm


def signup(request):
    """Basic user registration"""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
        else:
            form = RegistrationForm()
        return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def sign_in(request):
    """Login form"""
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
        else:
            form = AuthenticationForm()
            return render(request, 'accounts/signin.html', {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/signin.html', {"form": form})


def log_out(request):
    """Logout the user"""
    logout(request)
    return redirect('homepage')