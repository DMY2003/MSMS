"""Tests of the admin change balance view."""
from django.test import TestCase
from lessons.tests.helper import LogInTester
from django.urls import reverse
from lessons.models import Administrator, Request, Student, Lesson
from lessons.tests.helper import reverse_with_next


class AdminChangeBalanceTestCase(TestCase, LogInTester):
    """Tests of the admin change balance view."""

    fixtures = [
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_administrator.json'
    ]

    def setUp(self):
        self.url = reverse('change_balance', args=[2])
        self.user = Student.objects.get(email="janedoe@example.org")
        self.user2 = Administrator.objects.get(email='bob_green@email.com')

    def test_admin_change_balance_url(self):
        self.login(self.user2)
        self.assertEqual(self.url, "/administrator/change_balance/2")

    def test_admin_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/log_in/?next=/administrator/change_balance/2')
