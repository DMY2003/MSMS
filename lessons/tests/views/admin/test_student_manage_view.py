"""Tests of the student manage view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Administrator, Director
from lessons.tests.helper import LogInTester


class StudentManageViewTestCase(TestCase, LogInTester):
    """Tests of the student manage view."""

    fixtures = [
        'lessons/tests/fixtures/other_students.json',
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

    def test_get_student_manage_redirects_when_not_director_or_administrator(self):
        self.user = Student.objects.get(id=2)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_dashboard/student_requests.html')
