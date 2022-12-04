"""Unit tests of the create admin form."""
from django.test import TestCase
from django import forms
from lessons.forms import CreateAdminsForm
from lessons.models import Administrator, Student
from django.contrib.auth.hashers import check_password


class CreateAdminFormTestCase(TestCase):
    """Unit tests of the create admin form."""
    def setUp(self):
        self.form_input = {
            'first_name': 'Bob',
            'last_name': 'Green',
            'email': 'bob_green@email.com',
            'new_password': 'Password123',
            'confirm_password': 'Password123'
        }
    
    # default test
    def test_valid_create_admin_form(self):
        form = CreateAdminsForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_craete_admin_form_has_necessary_fields(self):
        form = CreateAdminsForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('confirm_password', form.fields)
        password_confirmation_widget = form.fields['confirm_password'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_create_admin_form_uses_model_validation(self):
        self.form_input['email'] = 'bademail'
        form = CreateAdminsForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_admin_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['confirm_password'] = 'password123'
        form = CreateAdminsForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['confirm_password'] = 'PASSWORD123'
        form = CreateAdminsForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['confirm_password'] = 'PasswordABC'
        form = CreateAdminsForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['confirm_password'] = 'WrongPassword123'
        form = CreateAdminsForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = CreateAdminsForm(data=self.form_input)
        before_count = Administrator.objects.count()
        form.save()
        after_count = Administrator.objects.count()
        self.assertEqual(after_count, before_count + 1)
        admin = Administrator.objects.get(email='bob_green@email.com')
        self.assertEqual(admin.first_name, 'Bob')
        self.assertEqual(admin.last_name, 'Green')
        is_password_correct = check_password('Password123', admin.password)
        self.assertTrue(is_password_correct)