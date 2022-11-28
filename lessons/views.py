from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm, RequestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


def login_prohibited(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('requests')
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


@login_prohibited
def home(request):
    return render(request, 'home.html')


@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('requests')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('requests')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('home')


@login_required
def requests(request):
    if request.user.role == 'Student':
        return render(request, 'student_requests_page.html')
    elif request.user.role == 'Administrator' or request.user.role == 'Director':
        return render(request, 'admin_requests_page.html')


@login_required
def transactions(request):
    if request.user.role == 'Student':
        return render(request, 'student_transactions_page.html')
    elif request.user.role == 'Administrator' or request.user.role == 'Director':
        return render(request, 'admin_transactions_page.html')


@login_required
def lessons(request):
    if request.user.role == 'Student':
        return render(request, 'student_lessons_page.html')


# -------------------------------NEW--------------------------------------
def make_request(request, form=None):
    if request.method == 'POST':
        print("Hello")
        form = RequestForm(request.POST)

        if not form.is_valid():
            form_data = form.cleaned_data
            details = [form_data.get("time_availability"), form_data.get("day_availability"),
                       form_data.get("lesson_interval"), form_data.get("lesson_count"),
                       form_data.get("lesson_duration"), form_data.get("preferred_teacher"),
                       form_data.get("instrument")]

            print(details)

            return redirect('new-request')

    return render(request, 'student_request_form2.html', {'form': form})
