"""Unit tests of the admin request form."""
from django.test import TestCase
from django import forms
from lessons.forms import AdminRequestForm
import datetime
from lessons.models import Teacher, Instrument, Request, Term


class AdminRequestFormTestCase(TestCase):
    """Unit tests of the admin request form."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_teacher.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_request.json',
        'lessons/tests/fixtures/default_term.json',
    ]

    def setUp(self):
        self.form_input = {
            "day_availability": 5,
            "time_availability": datetime.time(12, 30),
            "teacher": Teacher.objects.get(id=1),
            "lesson_duration": 30,
            'lesson_interval': 1,
            'lesson_count': 6,
            'instrument': Instrument.objects.get(id=1),
            'term': 2,
            'paid':0
        }

    def test_form_contains_required_fields(self):
        form = AdminRequestForm()
        self.assertIn('day_availability', form.fields)
        day_field = form.fields['day_availability']
        self.assertTrue(isinstance(day_field, forms.TypedChoiceField))
        self.assertIn('time_availability', form.fields)
        time_field = form.fields['time_availability']
        self.assertTrue(isinstance(time_field, forms.TimeField))
        self.assertIn('teacher', form.fields)
        teacher_field = form.fields['teacher']
        self.assertTrue(isinstance(teacher_field, forms.ModelChoiceField))
        self.assertIn('lesson_duration', form.fields)
        lesson_duration_field = form.fields['lesson_duration']
        self.assertTrue(isinstance(lesson_duration_field, forms.TypedChoiceField))
        self.assertIn('lesson_count', form.fields)
        lesson_count_field = form.fields['lesson_count']
        self.assertTrue(isinstance(lesson_count_field, forms.IntegerField))
        self.assertIn('lesson_interval', form.fields)
        lesson_interval_field = form.fields['lesson_interval']
        self.assertTrue(isinstance(lesson_interval_field, forms.TypedChoiceField))
        self.assertIn('instrument', form.fields)
        instrument_field = form.fields['instrument']
        self.assertTrue(isinstance(instrument_field, forms.ModelChoiceField))
        lesson_count_field = form.fields['lesson_count']
        self.assertTrue(isinstance(lesson_count_field, forms.IntegerField))

    def test_form_accepts_valid_input(self):
        form = AdminRequestForm(data=self.form_input)
        #print(form.errors)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['day_availability'] = 6
        form = AdminRequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_teacher_field_must_not_be_blank(self):
        self.form_input['teacher'] = None
        form = AdminRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        request = Request.objects.get(id=1)
        form = AdminRequestForm(instance=request, data=self.form_input)
        before_count = Request.objects.count()
        form.save()
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(request.instrument, Instrument.objects.get(id=1))
