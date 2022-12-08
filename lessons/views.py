import mimetypes
from django.http.response import HttpResponse
from itertools import chain
from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm, AdminRequestForm, UserForm, PasswordForm, AdminLessonForm, StudentRequestForm, \
    CreateAdminsForm, AccountForm, TermForm, ChildForm, ParentRequestForm, UpdateBalance
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from lessons.models import Request, Lesson, Student, Administrator, User, Term, Transaction, Child
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from lessons.helpers import login_prohibited, map_terms
from django.core.paginator import Paginator, EmptyPage
import datetime
from django.conf import settings


@login_prohibited
def home(request):
    '''The home page of the website.'''
    return render(request, 'home.html')


@login_prohibited
def sign_up(request):
    '''The sign up page of the website.'''
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
    '''The log in page of the website.'''
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
    '''Logs the user out.'''
    logout(request)
    return redirect('home')


@login_required
def password(request):
    '''The change password page of the website.'''
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
    '''The edit profile page of the website.'''
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
    '''The student requests page of the website.'''
    if request.user.role == 'Student':
        student = request.user.id

        children = Child.objects.filter(parent=student)
        confirmed_requests = Request.objects.filter(student_id=student, is_approved=True)
        unconfirmed_requests = Request.objects.filter(student_id=student, is_approved=False)

        for child in children:
            lesson_list = Request.objects.filter(student_id=child, is_approved=True)
            confirmed_requests = list(chain(confirmed_requests, lesson_list))

        for child in children:
            lesson_list = Request.objects.filter(student_id=child, is_approved=False)
            unconfirmed_requests = list(chain(unconfirmed_requests, lesson_list))

        response_data = {
            "form": StudentRequestForm(),
            "confirmed_requests": confirmed_requests,
            "ongoing_requests": unconfirmed_requests
        }

        return render(request, 'student_dashboard/student_requests.html', response_data)

    elif request.user.role == 'Administrator' or request.user.role == 'Director':
        return redirect('admin_lessons')


def admin_request_delete(request, request_id):
    """Handles the deletion of a particular request"""
    if request.user.role == 'Administrator' or request.user.role == 'Director':
        try:
            lesson_request = Request.objects.get(id=request_id)
            lesson_request.delete()
            messages.add_message(request, messages.ERROR, "The request has been successfully deleted!")
        except Request.DoesNotExist:
            pass
        return redirect("admin_unapproved_requests")

    else:
        return redirect('home')


@login_required
def admin_request(request, request_id):
    """Handles the display of a particular admin request and the functionality to
    generate lessons from it"""
    if request.user.role == 'Administrator' or request.user.role == 'Director':
        lesson_request = Request.objects.get(id=request_id)
        if request.method == "POST":
            form = AdminRequestForm(request.POST, instance=lesson_request)

            if form.is_valid():
                form.save()

                teacher = form.cleaned_data.get("teacher")
                term = form.cleaned_data.get("term")

                lesson_request.generate_lessons(
                    teacher,
                    term
                )

                messages.add_message(request, messages.SUCCESS, "Lessons successfuly booked!")
                return redirect("admin_unapproved_requests")
            messages.add_message(request, messages.ERROR, "The request cannot be approved with the details provided!")
        else:
            terms = Term.objects.filter(end_date__gte=datetime.datetime.now().date())
            first_term = None
            if len(terms) > 0:
                first_term = terms[0]
            form = AdminRequestForm(instance=lesson_request, initial={"term": first_term})

        return render(request, 'admin_dashboard/admin_request.html', {'form': form, 'request': lesson_request})
    else:
        return redirect('home')


@login_required
def admin_approved_requests(request):
    '''Handles the display of approved requests'''
    if request.user.role == 'Administrator' or request.user.role == 'Director':
        page_number = request.GET.get('page', 1)
        requests = Request.objects.filter(is_approved=True)
        paginator = Paginator(requests, settings.ADMIN_REQUESTS_PAGE_SIZE)
        requests_page = paginator.page(page_number)
        response_data = {"requests": requests_page}

        return render(request, 'admin_dashboard/admin_approved_requests.html', response_data)

    else:
        return redirect('home')


@login_required
def admin_unapproved_requests(request):
    '''Handles the display of unapproved requests'''
    if request.user.role == 'Administrator' or request.user.role == 'Director':
        page_number = request.GET.get('page', 1)
        requests = Request.objects.filter(is_approved=False)
        paginator = Paginator(requests, settings.ADMIN_REQUESTS_PAGE_SIZE)
        requests_page = paginator.page(page_number)
        response_data = {"requests": requests_page}
        return render(request, 'admin_dashboard/admin_unapproved_requests.html', response_data)

    else:
        return redirect('home')


@login_required
def admin_lessons(request):
    """Handles the display of lessons"""

    if request.user.role == 'Administrator' or request.user.role == 'Director':
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

        paginator = Paginator(lessons, settings.ADMIN_REQUESTS_PAGE_SIZE)

        try:
            lessons_page = paginator.page(page_number)
        except EmptyPage:
            lessons_page = []

        response_data = {
            "lessons": lessons_page,
            "lesson_count": len(lessons),
            "name_search": name_search
        }
        return render(request, 'admin_dashboard/admin_lessons.html', response_data)

    else:
        return redirect('home')


@login_required
def admin_lesson(request, lesson_id):
    """Handles the display and updating of a particular lesson"""
    if request.user.role == 'Administrator' or request.user.role == 'Director':
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
        return render(request, 'admin_dashboard/admin_lesson.html', response_data)

    else:
        return redirect('home')


@login_required
def admin_lesson_delete(request, lesson_id):
    """Handles the deletion of a particular lesson"""
    if request.user.role == 'Administrator' or request.user.role == 'Director':
        lesson = Lesson.objects.get(id=lesson_id)
        if lesson:
            lesson.delete()
        messages.add_message(request, messages.ERROR, "The lesson has been successfully deleted!")
        return redirect("admin_lessons")

    else:
        return redirect('home')


@login_required
def create_admin(request):
    """Handles the creation of a new admin"""
    if request.user.role == 'Director':
        if request.method == 'POST':
            form = CreateAdminsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Account created!")
                return redirect('manage_admins')
        else:
            form = CreateAdminsForm()
        return render(request, 'admin_dashboard/create_admin.html', {'form': form})
    elif request.user.role == 'Administrator':
        messages.add_message(request, messages.ERROR, "You do not have permission to manage admins!")
        return redirect('admin_lessons')


@login_required
def manage_admins(request):
    """Handles the display of all admins"""
    if request.user.role == 'Director':
        email_search = request.GET.get('email_search', None)
        accounts = Administrator.objects.all()
        if email_search:
            accounts = Administrator.objects.filter(
                email=email_search
            )

        response_data = {
            "accounts": accounts,
            "account_count": len(accounts),
            "email_search": email_search
        }
        return render(request, 'admin_dashboard/manage_admins.html', response_data)
    elif request.user.role == 'Administrator':
        messages.add_message(request, messages.ERROR, "You do not have permission to manage admins!")
        return redirect('admin_lessons')


@login_required
def manage_students(request):
    """Handles the display of all students"""
    if request.user.role == 'Director' or request.user.role == 'Administrator':
        email_search = request.GET.get('email_search', None)
        accounts = Student.objects.filter(child__isnull=True)
        if email_search:
            accounts = Student.objects.filter(
                email=email_search
            )

        response_data = {
            "accounts": accounts,
            "student_count": len(accounts),
            "email_search": email_search
        }
        return render(request, 'admin_dashboard/manage_students.html', response_data)
    else:
        messages.add_message(request, messages.ERROR, "You do not have permission to manage students!")
        return redirect('home')


@login_required
def edit_account(request, account_id):
    """Handles the display and updating of a particular account"""
    if request.user.role == 'Director':
        account = User.objects.get(id=account_id)
        if request.method == 'POST':
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Account updated!")
                return redirect('manage_admins')
        else:
            form = AccountForm(instance=account)
        return render(request, 'admin_dashboard/edit_account.html', {'form': form, 'account': account})
    else:
        messages.add_message(request, messages.ERROR, "You do not have permission to edit an admin!")
        return redirect("home")


@login_required
def manage_user_delete(request, user_id):
    """Handles the deletion of a particular user"""
    user = User.objects.get(id=user_id)
    role = user.role
    if user:
        user.delete()
    messages.add_message(request, messages.ERROR, "The account has been successfully deleted!")
    if request.user.role == "Administrator":
        return redirect("manage_students")
    elif request.user.role == "Director":
        if role == "Administrator":
            return redirect("manage_admins")
        elif role == "Student":
            return redirect("manage_students")


@login_required
def student_request_create(request):
    """Handles the creation of a request through the student request form"""
    quantity_children = len(Child.objects.filter(parent_id=request.user.id).values())

    if request.user.role != 'Student':
        return redirect('home')

    if quantity_children == 0:
        form = StudentRequestForm()
    else:
        form = ParentRequestForm(user=request.user)

    if request.method == 'POST':
        if quantity_children == 0:
            student = Student.objects.get(email=request.user.email)
            form = StudentRequestForm(preset_attrs={'student': student}, data=request.POST)
        else:
            form = ParentRequestForm(user=request.user, data=request.POST)

        lesson_request = form
        if form.is_valid():
            lesson_request.save()
            return redirect('student_requests')

    return render(request, 'student_dashboard/student_request_create.html', {'form': form})


@login_required
def student_request_update(request, request_id):
    """Handles the updating of a request through the student request form"""
    if request.user.role != 'Student':
        return redirect('home')

    lesson_request = Request.objects.get(pk=request_id)

    response_data = {
        "request": lesson_request
    }

    if request.method == "POST":
        form = StudentRequestForm(request.POST, instance=lesson_request)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Your request was successfully updated!")
            response_data["form"] = form
            return render(request, 'student_dashboard/student_request_update.html', response_data)
        messages.add_message(request, messages.ERROR, "Your request is not valid!")
    else:
        form = StudentRequestForm(instance=lesson_request)
        response_data["form"] = form

    return render(request, 'student_dashboard/student_request_update.html', response_data)


@login_required
def student_request_delete(request, request_id):
    """Handles the deletion of a request by the student who has made it"""
    if request.user.role != 'Student':
        return redirect('home')

    lesson_request = Request.objects.get(id=request_id)
    if lesson_request:
        messages.add_message(request, messages.SUCCESS, "Your request was successfully deleted!")
        lesson_request.delete()
    return redirect('student_requests')


@login_required
def student_lessons(request):
    """Handles the display of lessons for students"""
    if request.user.role != 'Student':
        return redirect('home')
    instrument_search = request.GET.get('instrument_search', None)
    page_number = request.GET.get('page', 1)
    page_number1 = request.GET.get('page1', 1)
    page_number2 = request.GET.get('page2', 1)

    lessons = Lesson.objects.filter(student=request.user)
    previous_lessons = Lesson.objects.filter(student=request.user, date__lte=datetime.datetime.now())
    upcoming_lessons = Lesson.objects.filter(student=request.user, date__gte=datetime.datetime.now())

    # Filters lessons by the name provided
    if instrument_search:
        upcoming_lessons = Lesson.objects.filter(
            instrument__name__contains=instrument_search,
            student=request.user,
            date__gte=datetime.datetime.now()
        )
        previous_lessons = Lesson.objects.filter(
            instrument__name__contains=instrument_search,
            student=request.user,
            date__lte=datetime.datetime.now()
        )

    paginator1 = Paginator(upcoming_lessons, 6)
    paginator2 = Paginator(previous_lessons, 6)

    try:
        upcoming_lessons_page = paginator1.page(page_number1)
        previous_lessons_page = paginator2.page(page_number2)
    except EmptyPage:
        upcoming_lessons_page = []
        previous_lessons_page = []

    response_data = {
        "upcoming_lessons": upcoming_lessons_page,
        "previous_lessons": previous_lessons_page,
        "lesson_count": len(lessons),
        "instrument_search": instrument_search
    }
    return render(request, 'student_dashboard/student_lessons.html', response_data)


@login_required
def term_create(request):
    """Handles the creation of a term"""
    if request.user.role != 'Director' and request.user.role != 'Administrator':
        return redirect('home')
    form = TermForm()

    if request.method == "POST":
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The term was successfully created!")

    terms = map_terms(Term.objects.all())

    response_data = {"terms": terms, "form": form}

    return render(request, 'admin_dashboard/term_create.html', response_data)


@login_required
def term_update(request, term_id):
    """Handles the updating of a term's start date and end date"""
    if request.user.role != 'Director' and request.user.role != 'Administrator':
        return redirect('home')
    term = Term.objects.get(pk=term_id)
    if request.method == "POST":
        form = TermForm(request.POST, instance=term)

        if form.is_valid():
            form.save() 
            messages.add_message(request, messages.SUCCESS, "The term was succesfully updated!")
            return redirect('term_create')
    else:
        form = TermForm(instance=term)

    terms = map_terms(Term.objects.all())

    term_position = 1
    for position, current_term in terms.items():
        if current_term == term:
            term_position = position

    response_data = {
        "terms": terms,
        "form": form,
        "term_position": term_position,
        "term": term
    }

    return render(request, 'admin_dashboard/term_update.html', response_data)


@login_required
def term_delete(request, term_id):
    """Handles the deletion of a term"""
    if not request.user or request.user.role != 'Director' and request.user.role != 'Administrator':
        return redirect('home')
    try:
        Term.objects.get(pk=term_id).delete()
        messages.add_message(request, messages.SUCCESS, "The term was succesfully deleted!")
    except Term.DoesNotExist:
        pass
    return redirect('term_create')


def download(request, invoice: str):
    # Define text file name
    filename = invoice
    # Open the file for reading content
    path = open(filename, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filename)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


@login_required
def add_child(request):
    """Handles the adding of a child to a student's account"""
    form = ChildForm()
    if request.method == 'POST':
        form = ChildForm(request.POST)

        if form.is_valid():
            child_request = form.save(commit=False)
            parent = Student.objects.get(email=request.user.email)
            child_request.parent = parent
            child_request.role = "Student"
            child_request.save()
            return redirect('student_requests')

    return render(request, 'student_dashboard/add_child_form.html', {'form': form})


@login_required
def change_balance(request, user_id):
    """Handles the changing of a student's balance by an administrator"""
    if request.user.role == 'Administrator' or request.user.role == 'Director':
        student = Student.objects.get(id=user_id)

        response_data = {
            "balance": student.balance,
            "name": student.first_name + " " + student.last_name,
        }

        if request.method == 'POST':
            form = UpdateBalance(data=request.POST, user=student)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Balance Updated!")
                return redirect('manage_students')
        else:
            form = UpdateBalance(user=student)

        response_data.update({"form": form})

        return render(request, 'admin_dashboard/change_balance.html', response_data)
    else:
        return redirect('home')


@login_required
def transaction_history(request):
    """Handles the creation of a student's transaction history page"""
    student = request.user.id

    children = Child.objects.filter(parent=student)
    transactions = list(Transaction.objects.filter(student_id=student))

    for child in children:
        child_transactions = Transaction.objects.filter(student_id=child)
        transactions = list(chain(transactions, child_transactions))

    transactions.sort(key=lambda x: x.id, reverse=False)

    response_data = {
        "transactions": transactions
    }

    return render(request, 'student_dashboard/student_transaction_history.html', response_data)
