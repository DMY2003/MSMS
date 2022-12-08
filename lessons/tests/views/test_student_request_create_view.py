"""Tests of the student request create view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Request
from lessons.forms import StudentRequestForm
from lessons.tests.helper import reverse_with_next
import datetime


class StudentRequestCreateViewTestCase(TestCase):
    """Tests of the student request create view."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_instrument.json',
    ]

    def setUp(self):
        self.user = Student.objects.get(email='johndoe@example.org')
        self.url = reverse('student_request_create')
        self.form_input = {
            'time_availability': datetime.time(hour=12, minute=30, second=00),
            'day_availability': 2,
            'lesson_interval': 1,
            'lesson_count': 3,
            'lesson_duration': 30,
            'preferred_teacher': 'request_create_view_test',
            'instrument': 2,
            'paid': 0
        }

    def test_student_request_create_url(self):
        self.assertEqual(self.url, '/requests/create')

    def test_get_student_request_create(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_request_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, StudentRequestForm))
        self.assertFalse(form.is_bound)

    def test_student_request_create_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_student_request_create_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        form = StudentRequestForm(data=self.form_input)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

        response = self.client.post(self.url, self.form_input, follow=True)
        request = Request.objects.get(preferred_teacher="request_create_view_test")
        self.assertTrue(request)
        response_url = reverse('student_requests')
        self.assertTemplateUsed(response, 'student_requests.html')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_requests.html')
        if (request):
            request.delete()

    def test_student_request_create_unsuccessful(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input["instrument"] = "Guitar"
        form = StudentRequestForm(data=self.form_input)
        print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice. That choice is not one of the available choices.")
        self.assertTemplateUsed(response, 'student_request_create.html')
