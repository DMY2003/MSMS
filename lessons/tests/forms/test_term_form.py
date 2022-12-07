"""Unit tests of the term form."""
from django import forms
from django.test import TestCase
from lessons.forms import TermForm
from lessons.models import Term
from datetime import datetime


class RequestFormTestCase(TestCase):
    """Unit tests of the term form."""
    fixtures = [
        'lessons/tests/fixtures/default_term.json'
    ]

    def setUp(self):
        self.form_input = {
            "start_date": datetime(2023, 5, 4),
            "end_date": datetime(2023, 8, 7)
        }

        self.term = Term.objects.first()
        self.term_to_delete = Term.objects.last()

    def test_valid_form(self):
        form = TermForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_valid_form_with_instance(self):
        form = TermForm(data=self.form_input, instance=self.term)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = TermForm()
        self.assertIn('start_date', form.fields)
        start_date_field = form.fields['start_date']
        self.assertTrue(isinstance(start_date_field, forms.DateField))
        self.assertIn('end_date', form.fields)
        end_date_field = form.fields['end_date']
        self.assertTrue(isinstance(end_date_field, forms.DateField))

    def test_end_date_after_start_date(self):
        original_date = self.form_input["start_date"]
        self.form_input["start_date"] = datetime(2023, 8, 10)
        form = TermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input["start_date"] = original_date

    