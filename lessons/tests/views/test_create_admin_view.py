"""Tests of the create admin view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.forms import AccountForm
from lessons.models import User, Administrator, Director
from lessons.tests.helper import LogInTester


class CreateAdminTestCase(TestCase, LogInTester):
    """Tests of the create admin view."""

    fixtures = ['lessons/tests/fixtures/default_director.json']

    def setUp(self):
        self.url = reverse('create_admin')
        self.user = Director.objects.get(email='alex_green@email.org')

    def test_create_admin_url(self):
        self.assertEqual(self.url, '/director/create_admin')

    def test_create_admin_view(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_admin.html')
        self.assertContains(response, 'Create a new Administrator account')
        self.assertContains(response, 'First name:')
        self.assertContains(response, 'Last name:')
        self.assertContains(response, 'Email:')
        self.assertContains(response, 'Password:')
        self.assertContains(response, 'Confirm password:')
        self.assertContains(response, 'Create account')
    
    def test_create_admin_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/log_in/?next=/director/create_admin')

    # def test_create_admin_view_redirects_to_manage_admins(self):
    #     self.login(self.user)
    #     response = self.client.post(self.url, {
    #         'first_name': 'Test',
    #         'last_name': 'Admin',
    #         'email': 'test.admin@example.org',
    #         'password': 'Password123',
    #         'confirm_password': 'Password123'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/director/manage_admins')
        