from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm, AdminRequestForm, UserForm, PasswordForm, AdminLessonForm, StudentRequestForm, CreateAdminsForm, AccountForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Request, Lesson, Student, Administrator, User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage

def login_prohibited(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            role = request.user.role 
            if role == "Administrator":
                return redirect('admin_unapproved_requests')
            else:
                return redirect('student_requests')
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
            return redirect('student_requests')
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
                return redirect('student_requests')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

@login_required
def password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('student_requests')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            return redirect('student_requests')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})

@login_required
def student_requests(request):
    if request.user.role == 'Student':
        student = request.user.id

        response_data = {
            "form": StudentRequestForm(),
            "confirmed_requests": Request.objects.filter(student_id=student, is_approved=True),
            "ongoing_requests": Request.objects.filter(student_id=student, is_approved=False)
        }

        return render(request, 'student_requests.html', response_data)

    elif request.user.role == 'Administrator' or request.user.role == 'Director':
        return redirect('admin_unapproved_requests')


@login_required
def transactions(request):
    if request.user.role == 'Student':
        return render(request, 'student_transactions_page.html')
    elif request.user.role == 'Administrator' or request.user.role == 'Director':
        return render(request, 'admin_transactions_page.html')

@login_required
def lessons(request):
    if request.user.role == 'Student':
        return redirect('student_lessons')
    elif request.user.role == 'Administrator' or request.user.role == 'Director':
        return redirect('admin_lessons')

@login_required
def admin_request_delete(request, request_id):
    """Handles the deletion of a particular request"""
    lesson_request = Request.objects.get(id=request_id)
    if lesson_request:
        lesson_request.delete()
    messages.add_message(request, messages.ERROR, "The request has been successfully deleted!")
    return redirect("admin_unapproved_requests")

@login_required
def admin_request(request, request_id):
    """Handles the display of a particular admin request and the functionality to
    generate lessons from it"""
    lesson_request = Request.objects.get(id=request_id)
    if request.method == "POST":
        form = AdminRequestForm(request.POST, instance=lesson_request)
        if form.is_valid():
            form.save()

            lesson_request.generate_lessons(
                form.cleaned_data.get("teacher")
            )

            messages.add_message(request, messages.SUCCESS, "Lessons successfuly booked!")
            return redirect("admin_unapproved_requests")
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    else:
        form = AdminRequestForm(instance=lesson_request)

    return render(request, 'admin_request.html', {'form': form, 'request': lesson_request})


@login_required 
def admin_approved_requests(request):
    page_number = request.GET.get('page', 1)
    requests = Request.objects.filter(is_approved=True)
    paginator = Paginator(requests, 9)
    requests_page = paginator.page(page_number)
    response_data = {"requests": requests_page}

    return render(request, 'admin_approved_requests.html', response_data)


@login_required 
def admin_unapproved_requests(request):
    page_number = request.GET.get('page', 1)
    requests = Request.objects.filter(is_approved=False)
    paginator = Paginator(requests, 9)
    requests_page = paginator.page(page_number)
    response_data = {"requests": requests_page}

    return render(request, 'admin_unapproved_requests.html', response_data)

@login_required
def admin_requests(request):
    response_data = {
        "form": AdminRequestForm(),
        "fulfilled_requests": Request.objects.filter(is_approved=True),
        "unfulfilled_requests": Request.objects.filter(is_approved=False)
    }

    return render(request, 'admin_requests.html', response_data)

@login_required
def admin_lessons(request):
    """Handles the display of lessons"""
    name_search = request.GET.get('name_search', None)
    page_number = request.GET.get('page', 1) 

    lessons = Lesson.objects.all()

    # Filters lessons by the name provided
    if name_search:
        names = name_search.split()
        first_name = names[0] if len(names) >= 1 else ''
        second_name = names[1] if len(names) >= 2 else ''
        lessons = Lesson.objects.filter(
            student__first_name__contains=first_name,
            student__last_name__contains=second_name
        )

    paginator = Paginator(lessons, 9)
    
    try:
        lessons_page = paginator.page(page_number)
    except EmptyPage:
        lessons_page = []

    response_data = {
        "lessons": lessons_page,
        "lesson_count": len(lessons),
        "name_search": name_search
    }
    return render(request, 'admin_lessons.html', response_data)

@login_required
def admin_lesson(request, lesson_id):
    """Handles the display and updating of a particular lesson"""
    lesson = Lesson.objects.get(id=lesson_id)

    if request.method == "POST":
        form = AdminLessonForm(request.POST, instance=lesson)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The lesson was successfully updated!")
    elif request.method == "GET":
        form = AdminLessonForm(instance=lesson)

    response_data = {
        "lesson": lesson,
        "form": form
    }
    return render(request, 'admin_lesson.html', response_data)

@login_required
def admin_lesson_delete(request, lesson_id):
    """Handles the deletion of a particular lesson"""
    lesson = Lesson.objects.get(id=lesson_id)
    if lesson:
        lesson.delete()
    messages.add_message(request, messages.ERROR, "The lesson has been successfully deleted!")
    return redirect("admin_lessons")

@login_required
def create_admin(request):
    if request.method == 'POST':
        form = CreateAdminsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Account created!")
            return redirect('manage_admins')
    else:
        form = CreateAdminsForm()
    return render(request, 'create_admin.html', {'form': form})

@login_required
def manage_admins(request):
    """Handles the display of all admins"""
    email_search = request.GET.get('email_search', None)
    accounts = Administrator.objects.all()
    if email_search:
        accounts = Administrator.objects.filter(
            email = email_search
        )

    response_data = {
        "accounts": accounts,
        "account_count": len(accounts),
        "email_search": email_search
    }
    return render(request, 'manage_admins.html', response_data)

@login_required
def delete_account(request, account_id):
    """Handles the deletion of a particular account"""
    account = User.objects.get(id=account_id)
    if account:
        account.delete()
    messages.add_message(request, messages.ERROR, "The account has been successfully deleted!")
    return redirect("manage_admins")

@login_required
def edit_account(request, account_id):
    """Handles the display and updating of a particular account"""
    account = User.objects.get(id=account_id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Account updated!")
            return redirect('manage_admins')
    else:
        form = AccountForm(instance=account)
    return render(request, 'edit_account.html', {'form': form, 'account': account})

@login_required
def student_request_create(request):
    """Handles the creation of a request through the student request form"""
    form = StudentRequestForm()
    if request.method == 'POST':
        form = StudentRequestForm(request.POST)
        
        if form.is_valid():
            lesson_request = form.save(commit=False)
            student = Student.objects.get(email=request.user.email)
            lesson_request.student = student
            lesson_request.save()
            return redirect('student_requests')

    return render(request, 'student_request_create.html', {'form': form})

@login_required
def student_request_update(request, request_id):
    """Handles the updating of a request through the student request form"""
    lesson_request = Request.objects.get(pk=request_id)

    response_data = {
        "request": lesson_request
    }

    if request.method == "POST":
        form = StudentRequestForm(request.POST, instance=lesson_request)
        print(form.is_valid())
        print(form.cleaned_data)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Your request was successfully updated!")
            response_data["form"] = form
            return render(request, 'student_request_update.html', response_data)
        messages.add_message(request, messages.ERROR, "Your request is not valid!")
    else:
        form = StudentRequestForm(instance=lesson_request)
        response_data["form"] = form

    return render(request, 'student_request_update.html', response_data)

@login_required
def student_request_delete(request, request_id):
    lesson_request = Request.objects.get(id=request_id)
    if lesson_request:
        messages.add_message(request, messages.SUCCESS, "Your request was successfully deleted!")
        lesson_request.delete()
    return redirect('student_requests')


@login_required
def student_lessons(request):
    """Handles the display of lessons for students"""
    instrument_search = request.GET.get('instrument_search', None)
    page_number = request.GET.get('page', 1) 

    lessons = Lesson.objects.filter(student=request.user)

    # Filters lessons by the name provided
    if instrument_search:
        lessons = Lesson.objects.filter(
            instrument__name__contains=instrument_search,
            student=request.user
        )

    paginator = Paginator(lessons, 9)
    
    try:
        lessons_page = paginator.page(page_number)
    except EmptyPage:
        lessons_page = []

    response_data = {
        "lessons": lessons_page,
        "lesson_count": len(lessons),
        "instrument_search": instrument_search
    }
    return render(request, 'student_lessons.html', response_data)
