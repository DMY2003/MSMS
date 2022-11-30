"""Unit tests of the admin request form."""
from django.test import TestCase
from django import forms
from lessons.forms import LogInForm
from django.conf import settings
import datetime
from lessons.models import Teacher, Student


class AdminRequestFormTestCase(TestCase):
    """Unit tests of the admin request form."""
    def setUp(self):
        

        self.form_input = {
            "day": 0,
            "time": datetime.time(12, 30),
            "teacher"
            "lesson_duration": 30,
        }

    def test_test(self):
        teacher = Student.objects.first()
        print(teacher)
        self.assertTrue(True)

    # def test_form_contains_required_fields(self):
    #     form = LogInForm()
    #     self.assertIn('email', form.fields)
    #     self.assertIn('password', form.fields)
    #     password_field = form.fields['password']
    #     self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    # def test_form_accepts_valid_input(self):
    #     form = LogInForm(data=self.form_input)
    #     self.assertTrue(form.is_valid())