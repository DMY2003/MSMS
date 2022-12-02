"""Tests of the sign-up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.forms import SignUpForm
from lessons.models import User, Student
from lessons.tests.helper import LogInTester


class SignUpViewTestCase(TestCase, LogInTester):
    """Tests of the sign-up view."""

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'new_password': 'Password123',
            'confirm_password': 'Password123'
        }

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    #basic tests
    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_sign_up(self):
        self.form_input['email'] = 'BAD_USERNAME'
        before_count = Student.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Student.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count = Student.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Student.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('student_requests')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_requests.html')
        user = Student.objects.get(email='janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())

    # redirect tests
    # def test_get_sign_up_redirects_when_logged_in(self):
    #     self.client.login(email=self.form_input['email'], password="Password123")
    #     response = self.client.get(self.url, follow=True)
    #     redirect_url = reverse('home')
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'home.html')

    # def test_post_sign_up_redirects_when_logged_in(self):
    #     self.client.login(email=self.form_input['email'], password="Password123")
    #     before_count = Student.objects.count()
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     after_count = Student.objects.count()
    #     self.assertEqual(after_count, before_count)
    #     redirect_url = reverse('home')
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'home.html')
