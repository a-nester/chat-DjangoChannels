from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse

# Create your views here.



def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('my:index'))
    
        else:
            print(form.errors)
    return render(request, 'users/login.html', {'form' : form})

def log_out(request):
    logout(request)
    return redirect(reverse('my:index'))

def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('my:index'))
        else:
            print(form.errors)
    return render(request, 'users/signup.html', {'form' : form})