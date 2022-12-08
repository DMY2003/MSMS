"""Tests of the admin requests view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Administrator, Request, Teacher
from lessons.tests.helper import LogInTester
from django.conf import settings

class AdminRequestsViewTestCase(TestCase, LogInTester):
    """Tests of the admin requests view."""

    fixtures = [
        'lessons/tests/fixtures/default_administrator.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/other_teachers.json',
    ] 

    def setUp(self):
        self.unapproved_requests_url = reverse('admin_unapproved_requests')
        self.approved_requests_url = reverse('admin_approved_requests')
        self.admin = Administrator.objects.get(email='bob_green@email.com')

    def test_get_unapproved_admin_requests(self):
        self.login(self.admin)
        response = self.client.get(self.unapproved_requests_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_unapproved_requests.html')

    def test_get_approved_admin_requests(self):
        self.login(self.admin)
        response = self.client.get(self.approved_requests_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_approved_requests.html')
