"""Unit tests of the user form."""
from django import forms
from django.test import TestCase
from lessons.forms import UserForm
from lessons.models import User, Student

class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json'
    ]

    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org'
        }

    def test_form_has_necessary_fields(self):
        form = UserForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))

    def test_valid_user_form(self):
        form = UserForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['email'] = 'badusername'
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = Student.objects.get(email='johndoe@example.org')
        form = UserForm(instance=user, data=self.form_input)
        before_count = Student.objects.count()
        form.save()
        after_count = Student.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
