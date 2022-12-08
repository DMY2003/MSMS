"""Unit tests of the Child form."""
from django import forms
from django.test import TestCase
from lessons.forms import ChildForm
from lessons.models import Student,Child


class ChildFormTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/other_students.json',
        ]

    def setUp(self):
        self.form_input = {
            'first_name': "test",
            'last_name': "child",
            'email': "testchild@example.org",
        }
    
    # default test
    def test_valid_child_form(self):
        form = ChildForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_request_form_has_necessary_fields(self):
        form = ChildForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['email'] = "badEmail"
        form = ChildForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = ChildForm(data=self.form_input)
        before_count = Child.objects.count()
        child = form.save(commit=False)
        child.parent = Student.objects.get(id=2)
        child.role = "Student"
        form.save()
        after_count = Child.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(child.first_name, 'test')
        self.assertEqual(child.last_name, "child")
        self.assertEqual(child.email, "testchild@example.org")