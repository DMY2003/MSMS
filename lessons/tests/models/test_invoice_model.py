"""Unit tests of the Invoice model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Invoice, Lesson

class InvoiceModelTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_teacher.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_request.json',
        'lessons/tests/fixtures/default_lesson.json',
        'lessons/tests/fixtures/default_invoice.json',
        'lessons/tests/fixtures/other_invoices.json',
        ]

    def setUp(self):
        self.invoice = Invoice.objects.get(id=1)

    # default test
    def test_valid_invoice(self):
        self._assert_invoice_is_valid()

    # price tests
    def test_price_must_not_be_blank(self):
        self.invoice.price = ''
        self._assert_invoice_is_invalid()
    
    def test_price_need_not_be_unique(self):
        second_invoice = Invoice.objects.get(id=2)
        self.invoice.price = second_invoice.price
        self._assert_invoice_is_valid()

    def test_price_must_be_a_number(self):
        self.invoice.price = 'one hundred'
        self._assert_invoice_is_invalid()
        self.invoice.price = ''
        self._assert_invoice_is_invalid()
        self.invoice.price = '100'
        self._assert_invoice_is_valid()
        self.invoice.price = 100
        self._assert_invoice_is_valid()

    # paid tests
    def test_paid_must_not_be_blank(self):
        self.invoice.paid = ''
        self._assert_invoice_is_invalid()
    
    def test_paid_need_not_be_unique(self):
        second_invoice = Invoice.objects.get(id=2)
        self.invoice.paid = second_invoice.paid
        self._assert_invoice_is_valid()

    def test_price_must_be_a_boolean(self):
        self.invoice.price = 'is paid'
        self._assert_invoice_is_invalid()
        self.invoice.price = ''
        self._assert_invoice_is_invalid()
        self.invoice.price = 1
        self._assert_invoice_is_valid()
        self.invoice.price = True
        self._assert_invoice_is_valid()

    # lesson
    def test_lesson_must_not_be_blank(self):
        self.invoice.lesson = None
        self._assert_invoice_is_invalid()
    
    def test_lesson_need_not_be_unique(self):
        second_invoice = Invoice.objects.get(id=2)
        self.invoice.lesson = second_invoice.lesson
        self._assert_invoice_is_valid()

    def test_student_must_be_an_instance_of_student_class(self):
        lesson = self.invoice.lesson
        self.assertIsInstance(lesson, Lesson)

    # helper functions
    def _assert_invoice_is_valid(self):
        try:
            self.invoice.full_clean()
        except ValidationError:
            self.fail('Test invoice should be valid')

    def _assert_invoice_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invoice.full_clean()