"""Unit tests of the admin lesson form."""
from django.test import TestCase
from django import forms
from lessons.forms import LogInForm
from django.conf import settings
import datetime
from lessons.models import Teacher, Student


class AdminLessonFormTestCase(TestCase):
    """Unit tests of the admin lesson form."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_teacher.json',
        'lessons/tests/fixtures/default_instrument.json',
    ]

    def setUp(self):
        self.form_input = {
            "day": 0,
            "time": datetime.time(12, 30),
            "teacher"
            "lesson_duration": 30,
        }

    def test_test(self):
        teacher = Student.objects.first()
        print(teacher)
        self.assertTrue(True)