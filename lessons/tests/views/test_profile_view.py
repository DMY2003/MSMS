"""Tests for the profile view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from lessons.forms import UserForm
from lessons.models import User, Student
from lessons.tests.helper import reverse_with_next

class ProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json'
    ]

    def setUp(self):
        self.user = Student.objects.get(email='johndoe@example.org')
        self.url = reverse('profile')
        self.form_input = {
            'first_name': 'John2',
            'last_name': 'Doe2',
            'email': 'johndoe2@example.org'
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_profile_update(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['email'] = 'BAD_EMAIL'
        before_count = Student.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Student.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')

    def test_unsuccessful_profile_update_due_to_duplicate_email(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['email'] = 'johndoe@example.org'
        before_count = Student.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Student.objects.count()
        self.assertEqual(after_count, before_count)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'johndoe@example.org')

    def test_succesful_profile_update(self):
        self.client.login(email=self.user.email, password='Password123')
        before_count = Student.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Student.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('student_requests')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_dashboard/student_requests.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'johndoe2@example.org')

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
