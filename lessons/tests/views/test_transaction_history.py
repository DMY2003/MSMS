"""Test of transaction history view"""

from django.test import TestCase
from django.urls import reverse
from lessons.tests.helper import LogInTester

from lessons.models import Student


class TransactionHistoryViewTestCase(TestCase, LogInTester):
    """Tests of the transaction history view."""

    fixtures = ['lessons/tests/fixtures/other_students.json']  # add fixture for request

    def setUp(self):
        self.url = reverse('transaction_history')
        self.user = Student.objects.get(email="janedoe@example.org")

    def test_student_transaction_history_url(self):
        self.login(self.user)
        self.assertEqual(self.url, '/student/transaction_history/')

    def test_transaction_history_view(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard/student_transaction_history.html')
        self.assertContains(response, 'Transaction History')