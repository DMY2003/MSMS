"""Tests of the student request update view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Request, Administrator
from lessons.forms import StudentRequestForm
from lessons.tests.helper import reverse_with_next
import datetime


class StudentRequestUpdateViewTestCase(TestCase):
    """Tests of the student request update view."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_request.json',
        'lessons/tests/fixtures/other_administrators.json',
    ]

    def setUp(self):
        self.user = Student.objects.get(email='johndoe@example.org')
        self.url = reverse('student_request_update', kwargs={'request_id': 1})
        self.form_input = {
            'time_availability': datetime.time(hour=12, minute=30, second=00),
            'day_availability': 5,
            'lesson_interval': 1,
            'lesson_count': 5,
            'lesson_duration': 30,
            'preferred_teacher': 'Tom Smith',
            'instrument': 1,
            'paid': 0
        }

    def test_student_request_update_url(self):
        self.assertEqual(self.url, '/requests/1')

    def test_get_student_request_update(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard/student_request_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, StudentRequestForm))
        self.assertFalse(form.is_bound)

    def test_student_request_update_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_student_request_update_parses_correct_request(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        request = response.context["request"]
        self.assertEqual(request.id, 1)
        self.assertEqual(request.preferred_teacher, "Tom Smith")

    def test_get_student_request_update_parses_form_is_instance_of_correct_request(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        request = response.context["request"]
        self.assertTrue(isinstance(form, StudentRequestForm))
        self.assertEqual(form.instance, request)

    def test_student_reqeust_update_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        request = Request.objects.get(id=1)

        self.assertTrue(request)
        self.assertEqual(request.lesson_count, 6)
        self.assertEqual(request.id, 1)

        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard/student_request_update.html')

        request = Request.objects.get(id=1)
        self.assertEqual(request.lesson_count, 5)
        self.assertEqual(request.id, 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your request was successfully updated!")

    def test_student_reqeust_update_unsuccessful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.form_input["instrument"] = 200

        request = Request.objects.get(id=1)

        self.assertTrue(request)
        self.assertEqual(request.instrument.name, "Piano")
        self.assertEqual(request.id, 1)

        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard/student_request_update.html')

        request = Request.objects.get(id=1)
        self.assertEqual(request.instrument.name, "Piano")
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your request is not valid!")

    def test_get_student_request_redirects_when_not_student(self):
        self.user = Administrator.objects.get(id=7)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('admin_unapproved_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_dashboard/admin_unapproved_requests.html')
