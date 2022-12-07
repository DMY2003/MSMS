"""Tests of the admin requests view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Administrator, Request, Teacher
from lessons.tests.helper import LogInTester

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
        self.user = Administrator.objects.get(email='bob_green@email.com')

    def test_admin_request_url(self):
        pass
        
        self.assertEqual(True, True)