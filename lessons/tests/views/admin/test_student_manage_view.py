"""Tests of the student manage view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Administrator, Director
from lessons.tests.helper import LogInTester


class StudentManageViewTestCase(TestCase, LogInTester):
    """Tests of the student manage view."""

    fixtures = [
        'lessons/tests/fixtures/default_administrator.json'
    ]

    def setUp(self):
        self.url = reverse('manage_students')
        self.user = Administrator.objects.get(email='bob_green@email.com')

    def test_student_manage_url(self):
        self.assertEqual(self.url, '/administrator/manage_students')

    def test_student_manage_view(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard/manage_students.html')
        self.assertContains(response, 'Manage Students')

    def test_student_manage_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/log_in/?next=/administrator/manage_students')
