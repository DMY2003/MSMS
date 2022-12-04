"""Unit tests of the sign-up form."""
from django import forms
from django.test import TestCase
from lessons.forms import StudentRequestForm
from lessons.models import User, Student, Instrument,Request
from django.contrib.auth.hashers import check_password
import datetime


class RequestFormTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_request.json',
        ]

    def setUp(self):
        self.form_input = {
            'time_availability': datetime.time(hour=12, minute=30, second=00),
            'day_availability': 5,
            'lesson_interval': 1,
            'lesson_count': 6,
            'lesson_duration': 30,
            'preferred_teacher': 'Tom Smith',
            'instrument': Instrument.objects.get(id=1)
        }
    
    # default test
    def test_valid_request_form(self):
        form = StudentRequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_request_form_has_necessary_fields(self):
        form = StudentRequestForm()
        self.assertIn('instrument', form.fields)
        instrument_field = form.fields['instrument']
        self.assertTrue(isinstance(instrument_field, forms.ModelChoiceField))
        self.assertIn('lesson_count', form.fields)
        lesson_count_field = form.fields['lesson_count']
        self.assertTrue(isinstance(lesson_count_field, forms.IntegerField))
        self.assertIn('lesson_interval', form.fields)
        lesson_interval_field= form.fields['lesson_interval']
        self.assertTrue(isinstance(lesson_interval_field, forms.TypedChoiceField))
        self.assertIn('lesson_duration', form.fields)
        duration_field = form.fields['lesson_duration']
        self.assertTrue(isinstance(duration_field, forms.TypedChoiceField))
        self.assertIn('time_availability', form.fields)
        time_availability_field= form.fields['time_availability']
        self.assertTrue(isinstance(time_availability_field, forms.TimeField))
        self.assertIn('day_availability', form.fields)
        day_availability_field= form.fields['day_availability']
        self.assertTrue(isinstance(day_availability_field, forms.TypedChoiceField))
        self.assertIn('preferred_teacher', form.fields)
        preferred_teacher_field= form.fields['preferred_teacher']
        self.assertTrue(isinstance(preferred_teacher_field, forms.CharField))

    def test_form_uses_model_validation(self):
        self.form_input['day_availability'] = 8
        form = StudentRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        request = Request.objects.get(id=1)
        form = StudentRequestForm(instance=request, data=self.form_input)
        before_count = Request.objects.count()
        form.save()
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(request.preferred_teacher, 'Tom Smith')
        self.assertEqual(request.instrument, Instrument.objects.get(id=1))
