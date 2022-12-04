"""Unit tests of the account form."""
from django.test import TestCase
from django import forms
from lessons.forms import AccountForm
from lessons.models import User, Administrator, Director
from django.contrib.auth.hashers import check_password


class AccountFormTestCase(TestCase):
    """Unit tests of the account form."""

    fixtures = ['lessons/tests/fixtures/default_administrator.json']

    def setUp(self):
        self.form_input = {
            'first_name': 'Bob',
            'last_name': 'Green',
            'email': 'bob_green@email.com',
            'role': 'Director'
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
        form.save()
        admin = User.objects.get(email='bob_green@email.com')
        self.assertEqual(admin.first_name, 'Bob')
        self.assertEqual(admin.last_name, 'Green')
        self.assertEqual(admin.role, 'Director')