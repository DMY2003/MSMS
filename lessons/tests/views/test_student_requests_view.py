"""Tests of the student requests view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Request
from lessons.forms import StudentRequestForm
from lessons.tests.helper import reverse_with_next

class StudentRequestsViewTestCase(TestCase):
    """Tests of the student requests view."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/other_requests.json',
        ]

    def setUp(self):
        self.user = Student.objects.get(email='johndoe@example.org')
        self.url = reverse('student_requests')

    def test_student_requests_url(self):
        self.assertEqual(self.url,'/student/requests')

    def test_get_student_requests(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_requests.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, StudentRequestForm))
        self.assertFalse(form.is_bound)

    def test_student_requests_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_student_requests_displays_requests_belonging_to_correct_student(self):
        self.client.login(email=self.user.email, password='Password123')
        request2 = Request.objects.get(id=1234)
        request3 = Request.objects.get(id=3000)
        response = self.client.get(self.url)
        self.assertContains(response, request3.id)
        self.assertNotContains(response, request2.id)

    def test_student_request_uses_correct_templates(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        templates = response.templates
        template_names = [template.name for template in templates]
        self.assertIn("student_requests.html", template_names)
        self.assertIn("base.html", template_names)
        self.assertIn("base_content.html", template_names)
        self.assertIn("partials/navbar.html", template_names)
        self.assertIn("partials/messages.html", template_names)
        self.assertIn("partials/student_request_table.html", template_names)

    def test_student_request_passes_correct_confirmed_requests_queryset(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        confirmed_requests = response.context["confirmed_requests"]
        self.assertEqual(len(confirmed_requests), 1)
        self.assertEqual(confirmed_requests[0].id, 3000)
    
    def test_student_request_passes_correct_ongoing_requests_queryset(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        ongoing_requests = response.context["ongoing_requests"]
        self.assertEqual(len(ongoing_requests), 1)
        self.assertEqual(ongoing_requests[0].id, 4000)