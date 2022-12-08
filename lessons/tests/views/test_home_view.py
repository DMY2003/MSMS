"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Student

class HomeViewTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ['lessons/tests/fixtures/default_student.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(email='johndoe@example.org')

    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_home_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_dashboard/student_requests.html')
