"""Unit tests of the Instrument model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Term

class InstrumentModelTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_term.json',
    ]

    def setUp(self):
        self.term = Term.objects.get(id=1)

    def test_term_instrument(self):
        self._assert_term_is_valid()

    def _assert_term_is_valid(self):
        try:
            self.term.full_clean()
        except ValidationError:
            self.fail('Test term should be valid')

    def test_start_date_need_not_be_unique(self):
        second_term = Term.objects.get(id=2)
        self.term.start_date = second_term.start_date
        self._assert_term_is_valid()

    def test_end_date_need_not_be_unique(self):
        second_term = Term.objects.get(id=2)
        self.term.end_date = second_term.end_date
        self._assert_term_is_valid()