"""Tests of the edit account view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Director
from lessons.tests.helper import LogInTester

class EditAccountViewTestCase(TestCase, LogInTester):
    """Tests of the edit account view."""

    fixtures = [
                'lessons/tests/fixtures/default_director.json',
                'lessons/tests/fixtures/default_administrator.json'
               ]

    def setUp(self):
        self.url = reverse('edit_account' , args=[1])
        self.user = Director.objects.get(email='alex_green@email.org')

    def test_admin_manage_url(self):
        self.assertEqual(self.url,'/edit_account/1')
    
    def test_admin_manage_view(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_account.html')
        self.assertContains(response, 'Edit account')
        self.assertContains(response, 'First name:')
        self.assertContains(response, 'Last name:')
        self.assertContains(response, 'Email:')
        self.assertContains(response, 'Role:')
        self.assertContains(response, 'Update')
        self.assertContains(response, 'Back')
    
    def test_admin_manage_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/log_in/?next=/edit_account/1')