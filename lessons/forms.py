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



class AdminRequestForm(forms.Form):
    """Handles the creation of lessons through the help of a lesson request"""
    start_date = forms.CharField(label="Day of the week")
    time = forms.TimeField(label="Time")
    teacher = forms.CharField(label="Teacher")
    lesson_count = forms.IntegerField(label="Number of lessons")
    lesson_duration = forms.IntegerField(label="Lesson duration")
    lesson_interval = forms.IntegerField(label="Lesson interval")
   
    def save(self):
        """Overrides save method in order to approve the request and generate the associated lessons"""
        request = super().save(commit=False)
        request.is_approved = True
        self.generate_lessons()
        request.save()
        return request

    def generate_lessons(self):
        pass

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

