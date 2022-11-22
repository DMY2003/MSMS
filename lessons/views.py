from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Administrator
from copy import deepcopy

def home(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('home')

@login_required(login_url='../log_in/')
def requests(request):
    if type(request.user).__class__ == Student:
        return render(request, 'student_requests_page.html')
    elif type(request.user) == Administrator:
        return render(request, 'admin_requests_page.html')

@login_required(login_url='../log_in/')
def transactions(request):
    if type(request.user) == Student:
        return render(request, 'student_transactions_page.html')
    elif type(request.user) == Administrator:
        return render(request, 'admin_transactions_page.html')

@login_required(login_url='../log_in/')
def lessons(request):
    if type(request.user) == Student:
        return render(request, 'student_lessons_page.html')

