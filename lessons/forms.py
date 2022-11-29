from django import forms
from lessons.models import User, Student, Teacher, Lesson
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

class LogInForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class AdminRequestForm(forms.Form):
    """Handles the creation of lessons through the help of a lesson request"""

    day = forms.ChoiceField(
        label="Day of the week",
        widget=forms.Select(),
        choices = settings.DAYS_OF_THE_WEEK,
    )   

    time = forms.TimeField(label="Time")

    teacher = forms.ModelChoiceField(
        label="Assigned teacher",
        queryset=Teacher.objects.all()
    )

    lesson_count = forms.IntegerField(label="Number of lessons")
    lesson_duration = forms.ChoiceField(
        label="Lesson duration",
        widget=forms.Select(),
        choices = settings.LESSON_DURATIONS,
    )   

    lesson_interval = forms.ChoiceField(
        label="Lesson intervals",
        widget=forms.Select(),
        choices = settings.LESSON_INTERVALS,
    )   
    def save(self):
        """Overrides save method in order to approve the request and generate the associated lessons"""
        request = super().save(commit=False)
        self.is_approved = True 
        self.generate_lessons()
        request.save()
        return request

    def get_date_from_weekday(self, weekday):
        """Gets the date from the weekday"""
        today = datetime.date.today().weekday()
        return today + datetime.timedelta(days=today - weekday)

    def generate_lessons(self):
        """Generates lessons on the provided day/time at weekly intervals"""
        teacher = Teacher.objects.get(email=self.teacher)
        lesson_datetime = self.get_date_from_weekday(self.day)
        for i in range(self.lesson_count):
            Lesson(teacher=teacher, student=self.student, time=lesson_datetime)
            lesson_datetime += datetime.timedelta(weeks=self.lesson_interval)