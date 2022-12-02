"""Unit tests of the Instrument model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Teacher, User

class TeacherModelTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_teacher.json',
        ]

    def setUp(self):
        self.teacher = Teacher.objects.get(id=1)

    # default test
    def test_valid_teacher(self):
        self._assert_teacher_is_valid()

    # other tests
    def test_str_method_returns_teachers_name(self):
        name = self.teacher.__str__()
        user = User.objects.get(id=1)
        self.assertEqual(name, user.full_name)

    # helper functions
    def _assert_teacher_is_valid(self):
        try:
            self.teacher.full_clean()
        except ValidationError:
            self.fail('Test teacher should be valid')

    def _assert_teacher_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.teacher.full_clean()