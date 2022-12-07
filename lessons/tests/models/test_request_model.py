"""Unit tests of the Request model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Request, Instrument, User, Student


class RequestModelTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_request.json',
        'lessons/tests/fixtures/other_requests.json',
    ]

    def setUp(self):
        self.request = Request.objects.get(id=1)

    # default test
    def test_valid_request(self):
        self._assert_request_is_valid()

    # Instrument tests
    def test_instrument_must_not_be_blank(self):
        self.request.instrument = None
        self._assert_request_is_invalid()

    def test_instrument_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.instrument = second_request.instrument
        self._assert_request_is_valid()

    def test_instrument_is_an_instance_of_instrument_class(self):
        self.assertIsInstance(self.request.instrument, Instrument)

    # #time_availability tests
    def test_time_availability_must_not_be_blank(self):
        self.request.time_availability = ''
        self._assert_request_is_invalid()

    def test_time_availability_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.time_availability = second_request.time_availability
        self._assert_request_is_valid()

    # day_availability tests
    def test_day_availability_cannot_be_blank(self):
        self.request.day_availability = ''
        self._assert_request_is_invalid()

    def test_day_availability_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.day_availability = second_request.day_availability
        self._assert_request_is_valid()

    # lesson_interval tests
    def test_lesson_interval_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.lesson_interval = second_request.lesson_interval
        self._assert_request_is_valid()

    def test_lesson_interval_must_be_an_integer(self):
        self.request.lesson_interval = 'two'
        self._assert_request_is_invalid()
        self.request.lesson_interval = ''
        self._assert_request_is_invalid()
        self.request.lesson_interval = '2'
        self._assert_request_is_valid()
        self.request.lesson_interval = 2
        self._assert_request_is_valid()

    # lesson_count tests
    def test_lesson_count_must_not_be_blank(self):
        self.request.lesson_count = ''
        self._assert_request_is_invalid()

    def test_lesson_count_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.lesson_count = second_request.lesson_count
        self._assert_request_is_valid()

    def test_lesson_count_must_be_a_number(self):
        self.request.lesson_interval = 'three'
        self._assert_request_is_invalid()
        self.request.lesson_interval = ''
        self._assert_request_is_invalid()

    # lesson_duration tests
    def test_lesson_duration_must_not_be_blank(self):
        self.request.lesson_duration = ''
        self._assert_request_is_invalid()

    def test_lesson_duration_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.lesson_duration = second_request.lesson_duration
        self._assert_request_is_valid()

    def test_lesson_duration_must_be_a_number(self):
        self.request.lesson_interval = 'sixty'
        self._assert_request_is_invalid()
        self.request.lesson_interval = ''
        self._assert_request_is_invalid()
        self.request.lesson_interval = '60'
        self._assert_request_is_invalid()
        self.request.lesson_interval = 1
        self._assert_request_is_valid()

    # preferred_teacher tests
    def test_preferred_teacher_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.preferred_teacher = second_request.preferred_teacher
        self._assert_request_is_valid()

    # student tests
    def test_student_must_not_be_blank(self):
        self.request.student = None
        self._assert_request_is_invalid()

    def test_student_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.student = second_request.student
        self._assert_request_is_valid()

    def test_student_must_be_an_instance_of_student(self):
        student = self.request.student
        self.assertIsInstance(student, Student)

    # is_approved tests
    def test_is_approved_must_not_be_blank(self):
        self.request.is_approved = ''
        self._assert_request_is_invalid()

    def test_is_approved_need_not_be_unique(self):
        second_request = Request.objects.get(id=2)
        self.request.is_approved = second_request.is_approved
        self._assert_request_is_valid()

    def test_is_approved_must_be_boolean(self):
        self.request.is_approved = 'approved'
        self._assert_request_is_invalid()

    # helper functions
    def _assert_request_is_valid(self):
        try:
            self.request.full_clean()
        except ValidationError:
            self.fail('Test Request should be valid')

    def _assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.request.full_clean()
