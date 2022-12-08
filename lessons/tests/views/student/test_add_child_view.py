"""Tests of the add child view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Child
from lessons.forms import ChildForm
from lessons.tests.helper import reverse_with_next
import datetime


class AddChildViewTestCase(TestCase):
    """Tests of the add child view."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_instrument.json',
    ]

    def setUp(self):
        self.user = Student.objects.get(email='johndoe@example.org')
        self.url = reverse('add_child')
        self.form_input = {
            'first_name': "test",
            'last_name': "child",
            'email': "testchild@example.org",
        }

    def test_add_child_url(self):
        self.assertEqual(self.url, '/student/add_child')

    def test_get_add_child(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard/add_child_form.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ChildForm))
        self.assertFalse(form.is_bound)

    def test_add_child_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_add_child_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        form = ChildForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

        before_count = Child.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Child.objects.count()
        self.assertEqual(before_count, after_count-1)
        response_url = reverse('student_requests')
        self.assertTemplateUsed(response, 'student_dashboard/student_requests.html')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_dashboard/student_requests.html')