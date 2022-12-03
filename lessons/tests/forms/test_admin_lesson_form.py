"""Unit tests of the admin lesson form."""
from django.test import TestCase
from django import forms
from lessons.forms import LogInForm
from django.conf import settings
import datetime
from lessons.models import Teacher, Student, Instrument, Lesson
from lessons.forms import AdminLessonForm


class AdminLessonFormTestCase(TestCase):
    """Unit tests of the admin lesson form."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_instrument.json'
    ]

    def setUp(self):
        self.student = Student.objects.first()
        self.instrument = Instrument.objects.first()

        teacher = Teacher.objects.create_user(
            first_name="Tony",
            last_name="Doe",
            username="",
            email="tony_doe@email.com",
            password="Password123"
        )

        teacher.role = "Teacher"
        teacher.save()
        self.teacher = teacher

        self.lesson = Lesson(
            teacher=teacher,
            student=self.student,
            date=datetime.datetime.now(),
            instrument=self.instrument,
            duration=30
        )
        self.lesson.student = self.student 
        self.lesson.save()

        self.form_input = {
            "date": datetime.datetime.now(),
            "teacher": self.teacher,
            "instrument": self.instrument,
            "duration": 45,
        }

    def test_form_contains_required_fields(self):
        form = AdminLessonForm(instance=self.lesson, data=self.form_input)
        self.assertIn('date', form.fields)
        self.assertIn('teacher', form.fields)
        self.assertIn('instrument', form.fields)
        self.assertIn('duration', form.fields)

    def test_form_accepts_valid_input(self):
        form = AdminLessonForm(instance=self.lesson, data=self.form_input)
        self.assertTrue(form.is_valid())
