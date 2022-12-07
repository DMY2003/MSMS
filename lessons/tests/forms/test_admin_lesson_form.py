"""Unit tests of the admin lesson form."""
from django.test import TestCase
from django import forms
from lessons.forms import AdminLessonForm
import datetime
from lessons.models import Teacher, Instrument, Lesson


class AdminLessonFormTestCase(TestCase):
    """Unit tests of the admin lesson form."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_teacher.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_request.json',
        'lessons/tests/fixtures/default_lesson.json',
        ]

    def setUp(self):
        self.form_input = {
            "date": datetime.datetime(year=2022,month=11,day=9,hour=12,minute=30,second=00),
            "duration": 30,
            "teacher": Teacher.objects.get(id=1),
            'instrument': Instrument.objects.get(id=1)
        }

    def test_admin_lesson_form_contains_required_fields(self):
        form = AdminLessonForm()
        self.assertIn('date', form.fields)
        date_field = form.fields['date']
        self.assertTrue(isinstance(date_field, forms.DateTimeField))
        self.assertIn('teacher', form.fields)
        teacher_field = form.fields['teacher']
        self.assertTrue(isinstance(teacher_field, forms.ModelChoiceField))
        self.assertIn('duration', form.fields)
        duration_field = form.fields['duration']
        self.assertTrue(isinstance(duration_field, forms.TypedChoiceField))
        self.assertIn('instrument', form.fields)
        instrument_field = form.fields['instrument']
        self.assertTrue(isinstance(instrument_field, forms.ModelChoiceField))


    def test_admin_lesson_form_accepts_valid_input(self):
        form = AdminLessonForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_admin_form_uses_model_validation(self):
        self.form_input['teacher'] = None
        form = AdminLessonForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_admin_lesson_form_must_save_correctly(self):
        lesson = Lesson.objects.get(id=1)
        form = AdminLessonForm(instance=lesson, data=self.form_input)
        before_count = Lesson.objects.count()
        form.save()
        after_count = Lesson.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(lesson.teacher, Teacher.objects.get(id=1))
        self.assertEqual(lesson.instrument, Instrument.objects.get(id=1))