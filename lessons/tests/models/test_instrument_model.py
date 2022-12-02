"""Unit tests of the Instrument model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Instrument

class InstrumentModelTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_teacher.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_lesson.json',
        ]

    def setUp(self):
        self.instrument = Instrument.objects.get(id=1)

    # default test
    def test_valid_instrument(self):
        self._assert_instrument_is_valid()

    # name tests
    def test_instrument_name_must_not_be_blank(self):
        self.instrument.name = ''
        self._assert_instrument_is_invalid()

    def test_instrument_name_need_not_be_unique(self):
        second_instrument = Instrument.objects.get(id=2)
        self.instrument.name = second_instrument.name
        self._assert_instrument_is_valid()

    def test_instrument_name_may_contain_30_characters(self):
        self.instrument.name = 'x' * 30
        self._assert_instrument_is_valid()

    def test_instrument_name_must_not_contain_more_than_30_characters(self):
        self.instrument.name = 'x' * 31
        self._assert_instrument_is_invalid()
    
    # helper functions
    def _assert_instrument_is_valid(self):
        try:
            self.instrument.full_clean()
        except ValidationError:
            self.fail('Test instrument should be valid')

    def _assert_instrument_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.instrument.full_clean()