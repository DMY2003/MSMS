from django import forms
from lessons.models import User, Student, Teacher, Instrument, Request, Lesson
from django.core.validators import RegexValidator
from django.conf import settings
import datetime

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

    field_order=["first_name", "last_name", "email", "new_password", "confirm_password"]

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

class AdminLessonForm(forms.Form):
    """Handles the input for updating a lesson"""

    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    ) 

    teacher = forms.ModelChoiceField(
        label="Assigned teacher",
        queryset=Teacher.objects.all(),

    )

    instrument = forms.ModelChoiceField(
        label="Assigned instrument",
        queryset=Instrument.objects.all(),       
    )

    lesson_duration = forms.ChoiceField(
        label="Lesson duration",
        widget=forms.Select(),
        choices = settings.LESSON_DURATIONS,
    )   


class AdminRequestForm(forms.Form):
    """Handles the creation of lessons through the help of a lesson request"""

    day = forms.ChoiceField(
        label="Day of the week",
        widget=forms.Select(),
        choices = settings.DAYS_OF_THE_WEEK,
    )   

    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    teacher = forms.ModelChoiceField(
        label="Assigned teacher",
        queryset=Teacher.objects.all(),

    )

    instrument = forms.ModelChoiceField(
        label="Assigned instrument",
        queryset=Instrument.objects.all(),       
    )

    lesson_count = forms.IntegerField(label="Number of lessons")
    lesson_duration = forms.ChoiceField(
        label="Lesson duration",
        widget=forms.Select(),
        choices = settings.LESSON_DURATIONS,
    )   

    lesson_interval = forms.ChoiceField(
        label="Lesson interval",
        widget=forms.Select(),
        choices = settings.LESSON_INTERVALS,
    )   

class RequestForm(forms.ModelForm):
    student = forms.IntegerField()
    instrument = forms.CharField()
    preferred_teacher = forms.CharField(required=False)

    class Meta:
        model = Request
        exclude = ['is_approved']

    def clean(self):
        cleaned_data = super(RequestForm, self).clean()

        requested = self.data.get("instrument")
        cleaned_data["instrument"] = Instrument.objects.get(name=requested)

        student_id = self.data.get("student")
        cleaned_data["student"] = Student.objects.get(id=student_id)

        return cleaned_data

class AdminLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson 
        fields = ["date", "teacher", "instrument", "duration"]
        widgets = {"date": forms.DateTimeInput(attrs={'type': 'date'})}

    # date = forms.DateTimeField(label="Edit date")


