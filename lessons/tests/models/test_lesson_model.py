"""Unit tests of the Lesson model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Lesson, Student, User, Teacher, Instrument
import datetime


class LessonModelTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_teacher.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_request.json',
        'lessons/tests/fixtures/default_lesson.json',
    ]

    def setUp(self):
        self.lesson = Lesson.objects.get(id=1)

    # default test
    def test_valid_lesson(self):

        self._assert_lesson_is_valid()

    # date tests
    def test_date_must_not_be_blank(self):
        self.lesson.date = ''
        self._assert_lesson_is_invalid()

    def test_date_need_not_be_unique(self):
        second_lesson = Lesson.objects.get(id=2)
        self.lesson.date = second_lesson.date
        self._assert_lesson_is_valid()

    def test_date_must_be_an_instance_of_datetime_class(self):
        self.assertIsInstance(self.lesson.date, datetime.datetime)

    # teacher tests
    def test_teacher_must_not_be_blank(self):
        self.lesson.teacher = None
        self._assert_lesson_is_invalid()

    def test_teacher_need_not_be_unique(self):
        second_lesson = Lesson.objects.get(id=2)
        self.lesson.teacher = second_lesson.teacher
        self._assert_lesson_is_valid()

    def test_teacher_must_be_an_instance_of_teacher_class(self):
        teacher = self.lesson.teacher
        self.assertIsInstance(teacher, Teacher)

    # student tests
    def test_student_must_not_be_blank(self):
        self.lesson.student = None
        self._assert_lesson_is_invalid()

    def test_student_need_not_be_unique(self):
        second_lesson = Lesson.objects.get(id=2)
        self.lesson.student = second_lesson.student
        self._assert_lesson_is_valid()

    def test_student_must_be_an_instance_of_student_class(self):
        student = self.lesson.student
        self.assertIsInstance(student, Student)

    # instrument tests
    def test_instrument_must_not_be_blank(self):
        self.lesson.instrument = None
        self._assert_lesson_is_invalid()

    def test_instrument_need_not_be_unique(self):
        second_lesson = Lesson.objects.get(id=2)
        self.lesson.instrument = second_lesson.instrument
        self._assert_lesson_is_valid()

    def test_instrument_must_be_an_instance_of_instrument_class(self):
        instrument = self.lesson.instrument
        self.assertIsInstance(instrument, Instrument)

    # duration tests
    def test_duration_must_not_be_blank(self):
        self.lesson.duration = ''
        self._assert_lesson_is_invalid()

    def test_duration_need_not_be_unique(self):
        second_lesson = Lesson.objects.get(id=2)
        self.lesson.duration = second_lesson.duration
        self._assert_lesson_is_valid()

    def test_duration_must_be_a_number(self):
        self.lesson.duration = 'sixty'
        self._assert_lesson_is_invalid()
        self.lesson.duration = ''
        self._assert_lesson_is_invalid()
        self.lesson.duration = '60'
        self._assert_lesson_is_valid()
        self.lesson.duration = 60
        self._assert_lesson_is_valid()

    def test_duration_must_be_a_valid_choice(self):
        self.lesson.duration = 60
        self._assert_lesson_is_valid()
        self.lesson.duration = 30
        self._assert_lesson_is_valid()
        self.lesson.duration = 45
        self._assert_lesson_is_valid()
        self.lesson.duration = 50
        self._assert_lesson_is_invalid()
        self.lesson.duration = 1
        self._assert_lesson_is_invalid()

    # helper functions
    def _assert_lesson_is_valid(self):
        try:
            self.lesson.full_clean()
        except ValidationError:
            self.fail('Test lesson should be valid')

    def _assert_lesson_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()
