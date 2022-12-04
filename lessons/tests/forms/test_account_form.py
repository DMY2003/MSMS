"""Unit tests of the account form."""
from django.test import TestCase
from django import forms
from lessons.forms import AccountForm
from lessons.models import Administrator, Student, User
from django.contrib.auth.hashers import check_password


class AccountFormTestCase(TestCase):
    """Unit tests of the account form."""
    def setUp(self):
        self.form_input = {
            'first_name': 'Bob',
            'last_name': 'Green',
            'email': 'bob_green@email.com',
            'role': 'Student'
        }
    
    def test_valid_account_form(self):
        form = AccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_account_form_has_necessary_fields(self):
        form = AccountForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('role', form.fields)
    
    def test_account_form_uses_model_validation(self):
        self.form_input['email'] = 'bademail'
        form = AccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly(self):
        form = AccountForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        admin = User.objects.get(email='bob_green@email.com')
        self.assertEqual(admin.first_name, 'Bob')
        self.assertEqual(admin.last_name, 'Green')