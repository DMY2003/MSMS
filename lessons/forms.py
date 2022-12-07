from django import forms
from lessons.models import User, Student, Administrator, Teacher, Instrument, Request, Lesson, Term, Transaction
from django.core.validators import RegexValidator
from django.conf import settings


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = {"first_name", "last_name", "email"}

    new_password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z](?=.*[a-z])(?=.*[0-9])).*$',
                message="Password must contain an uppercase character, a lowercase character and a number."
            )
        ]
    )
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            self.add_error("confirm_password", "Confirmation does not match password.")

    def save(self):
        super().save(commit=False)
        user = Student.objects.create_user(
            username=self.cleaned_data.get("email"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("new_password"),
        )
        user.role = "Student"
        user.save()
        return user

    field_order = ["first_name", "last_name", "email", "new_password", "confirm_password"]


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'email']


class PasswordForm(forms.Form):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class LogInForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class StudentRequestForm(forms.ModelForm):
    class Meta:
        model = Request

        exclude = [
            "is_approved", "teacher", "student"
        ]

        widgets = {
            "time_availability": forms.TimeInput(attrs={'type': 'time'})
        }


class AdminRequestForm(forms.ModelForm):
    class Meta:
        model = Request

        exclude = [
            "student", "is_approved", "preferred_teacher"
        ]

        widgets = {
            "time_availability": forms.TimeInput(attrs={'type': 'time'})
        }

    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), blank=False)


class AdminLessonForm(forms.ModelForm):
    """Implements a form for administrators to edit lessons"""

    class Meta:
        model = Lesson
        fields = ["date", "teacher", "instrument", "duration"]
        widgets = {"date": forms.DateTimeInput(attrs={'type': 'date'})}


class CreateAdminsForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = {"first_name", "last_name", "email"}

    new_password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z](?=.*[a-z])(?=.*[0-9])).*$',
                message="Password must contain an uppercase character, a lowercase character and a number."
            )
        ]
    )
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            self.add_error("confirm_password", "Confirmation does not match password.")

    def save(self):
        super().save(commit=False)
        user = Administrator.objects.create_user(
            username=self.cleaned_data.get("email"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("new_password"),
        )
        user.role = "Administrator"
        user.save()
        return user

    field_order = ["first_name", "last_name", "email", "new_password", "confirm_password"]


class AccountForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'email', 'role']

    role = forms.ChoiceField(choices=settings.ROLES)


class TermForm(forms.ModelForm):
    """Form to update school terms"""

    class Meta:
        """Form options"""

        model = Term
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateTimeInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            ),
            "end_date": forms.DateTimeInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            )
        }

    def clean(self):
        super().clean()

        if self.cleaned_data.get("start_date") > self.cleaned_data.get("end_date"):
            self.add_error("start_date", "Start date cannot come after end date!")
            self.add_error("end_date", "End date cannot come before start date!")
            return

        current_terms = Term.objects.all()

        for term in current_terms:
            if self.cleaned_data.get("start_date") <= term.end_date and self.cleaned_data.get(
                    "end_date") >= term.start_date:
                if self.instance:
                    if self.instance.id == term.id:
                        continue

                self.add_error("start_date", "Dates cannot overlap with current term dates!")
                self.add_error("end_date", "Dates cannot overlap with current term dates!")
                return


class ChildForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email"]

    def save(self):
        super().save(commit=False)
        user = Student.objects.create_user(
            username=self.cleaned_data.get("email"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email"),
        )
        user.role = "Student"
        user.save()
        return user

    field_order = ["first_name", "last_name", "email"]


class ParentRequestForm(StudentRequestForm):
    def __init__(self, user, *args, **kwargs):
        super(ParentRequestForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(parent=user)

    student = forms.ModelChoiceField(queryset=None)

    field_order = ["student"]

    def save(self):
        request = super().save(commit=False)

        request.student = self.cleaned_data["student"]

        request.save()
        return request

class UpdateBalance(forms.ModelForm):
    note = forms.CharField(label="Note", required=False, max_length=25)

    class Meta:
        model = Student
        fields = ['balance']

        labels = {
            'balance': 'Amount',
        }

    def save(self):
        student = super().save(commit=False)
        transaction_type = ""
        amount = self.cleaned_data["balance"]

        if "Subtract" in self.data:
            transaction_type = f"-£{amount}"
            student.balance = self.initial["balance"] - amount
        elif "Add" in self.data:
            transaction_type = f"+£{amount}"
            student.balance = self.initial["balance"] + amount
        elif "Change" in self.data:
            transaction_type = f"Set £{amount}"
            student.balance = amount

        Transaction.objects.create(student=student,
                                   note=self.cleaned_data["note"],
                                   change=transaction_type,
                                   old_balance=self.initial["balance"],
                                   new_balance=student.balance
                                   )
        student.save()
        return student
