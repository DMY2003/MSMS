from django import forms
from lessons.models import User, Student, Request, Instrument
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

DURATIONS = [(30, 30),
             (60, 60),
             (90, 90),
             (120, 120),
             (150, 150),
             (180, 180)]

DAYS = [("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
        ("saturday", "Saturday"),
        ("sunday", "Sunday")]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        exclude = ['student', 'is_approved']

