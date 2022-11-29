from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm, AdminRequestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Request
from django.contrib.auth.decorators import login_required, user_passes_test

def login_prohibited(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('requests')
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
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
    return redirect('sign_up')

@login_required
def requests(request):
    if request.user.role == 'Student':
        return render(request, 'student_requests_page.html')
    elif request.user.role == 'Administrator' or request.user.role == 'Director':
        return redirect('admin_requests')
@login_required
def transactions(request):
    if request.user.role == 'Student':
        return render(request, 'student_transactions_page.html')
    elif request.user.role == 'Administrator' or request.user.role == 'Director':
        return render(request, 'admin_transactions_page.html')

def admin_request_delete(request, request_id):
    print("delete")
    lesson_request = Request.objects.get(id=request_id)
    if lesson_request:
        lesson_request.delete()
    messages.add_message(request, messages.ERROR, "The request has been successfully deleted!")
    return redirect(request, "admin_requests")

def admin_request(request, request_id):
    lesson_request = Request.objects.get(id=request_id)
    if request.method == "POST":
        form = AdminRequestForm(request.POST)
        if form.is_valid():
            lesson_request.generate_lessons(form)
            lesson_request.save()
            return redirect("admin_requests")
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    else:
        form = AdminRequestForm()
    
    return render(request, 'admin_request.html', {'form': form, 'request': lesson_request})

def admin_requests(request):
    response_data = {
        "form": AdminRequestForm(),
        "fulfilled_requests": Request.objects.filter(is_approved=True),
        "unfulfilled_requests": Request.objects.filter(is_approved=False)
    }

    return render(request, 'admin_requests.html', response_data)


@login_required
def lessons(request):
    if request.user.role == 'Student':
        return render(request, 'student_lessons_page.html')

