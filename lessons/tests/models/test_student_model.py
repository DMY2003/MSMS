"""Unit tests of the Student model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Student, User

class StudentModelTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        ]

    def setUp(self):
        self.student = Student.objects.get(id=1)

    # default test
    def test_valid_student(self):
        self._assert_student_is_valid()

    # balance tests
    def test_balance_must_be_a_number(self):
        self.student.balance = 'one hundred'
        self._assert_student_is_invalid()
        self.student.balance = ''
        self._assert_student_is_invalid()
        self.student.balance = '100'
        self._assert_student_is_valid()
        self.student.balance = 100
        self._assert_student_is_valid()

    # helper functions
    def _assert_student_is_valid(self):
        try:
            self.student.full_clean()
        except ValidationError:
            self.fail('Test student should be valid')

    def _assert_student_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.student.full_clean()