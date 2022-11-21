from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
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

def student_requests(request):
    return render(request, 'student_requests_page.html')

def student_lessons(request):
    return render(request, 'student_lessons_page.html')

def student_transactions(request):
    return render(request, 'student_transactions_page.html')

def admin_requests(request):
    return render(request, 'admin_requests_page.html')

def admin_transactions(request):
    return render(request, 'admin_transactions_page.html')
