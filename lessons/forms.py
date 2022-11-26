from django import forms
from lessons.models import User, Student, Request
from django.core.validators import RegexValidator


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


class LogInForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


INSTRUMENTS = [("guitar", "Guitar"),
               ("ukulele", "Ukulele"),
               ("violin", "Violin"),
               ("recorder", "Recorder"),
               ("piano", "Piano"),
               ("triangle", "Triangle")]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['student_availability',
                  'lesson_count',
                  'lesson_duration',
                  'lesson_interval',
                  'preferred_teacher',
                  'instrument']

    student_availability = forms.DateTimeField(label="Availability")
    lesson_count = forms.IntegerField(label="Number of Lessons")
    lesson_duration = forms.IntegerField(label="Duration")
    lesson_interval = forms.CharField(label='Interval', widget=forms.Select(choices=[(1, 1), (2, 2)]))
    preferred_teacher = forms.CharField(label="Preferred Teacher")
    instrument = forms.CharField(label='Instrument', widget=forms.Select(choices=INSTRUMENTS))
