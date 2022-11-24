from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, user_passes_test


@user_passes_test(lambda user: not user.username, login_url='../requests', redirect_field_name=None)
def home(request):
    return render(request, 'home.html')

@user_passes_test(lambda user: not user.username, login_url='../requests', redirect_field_name=None)
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


@user_passes_test(lambda user: not user.username, login_url='../requests', redirect_field_name=None)
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
    elif  request.user.role == 'Administrator':
        return render(request, 'admin_requests_page.html')
    else:
        return render(request, 'home.html')

@login_required
def transactions(request):
    if request.user.role == 'Student':
        return render(request, 'student_transactions_page.html')
    elif request.user.role == 'Administrator':
        return render(request, 'admin_transactions_page.html')
    else:
        return render(request, 'home.html')

@login_required
def lessons(request):
    if request.user.role == 'Student':
        return render(request, 'student_lessons_page.html')
    else:
        return render(request, 'home.html')

