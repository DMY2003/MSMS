"""Tests of the log-out view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Student
from lessons.tests.helper import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):
    """Tests of the log-out view."""

    def setUp(self):
        self.url = reverse('log_out')
        self.user = Student.objects.create_user(
            email='johndoe@example.org',
            first_name='John',
            last_name='Doe',
            password='Password123',
        )

    def test_log_out_url(self):
        self.assertEqual(self.url,'/log_out/')

    # basic test
    def test_get_log_out(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('sign_up')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertFalse(self._is_logged_in())

    #redirect test
    def test_get_log_out_without_being_logged_in(self):
        response = self.client.get(self.url, follow=True)
        response_url = reverse('sign_up')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertFalse(self._is_logged_in())
