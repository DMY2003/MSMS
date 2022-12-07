"""Tests of the admin request view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Administrator, Request
from lessons.tests.helper import LogInTester

class AdminRequestViewTestCase(TestCase, LogInTester):
    """Tests of the admin request view."""

    fixtures = ['lessons/tests/fixtures/default_administrator.json'] # add fixture for request

    def setUp(self):
        self.url = reverse('admin_request', args=[1])
        self.user = Administrator.objects.get(email='bob_green@email.com')

    def test_admin_request_url(self):
        self.assertEqual(self.url,'/administrator/requests/1')

    # def test_admin_request_view(self):
    #     self.login(self.user)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'admin_request.html')
    #     self.assertContains(response, 'Request Administrator Account')
    #     self.assertContains(response, 'First name:')
    #     self.assertContains(response, 'Last name:')
    #     self.assertContains(response, 'Email:')
    #     self.assertContains(response, 'Request')

    def test_admin_request_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/log_in/?next=/administrator/requests/1')