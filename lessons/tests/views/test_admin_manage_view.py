"""Tests of the admin manage view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Director, Administrator
from lessons.tests.helper import LogInTester


class AdminManageViewTestCase(TestCase, LogInTester):
    """Tests of the admin manage view."""

    fixtures = [
                'lessons/tests/fixtures/default_director.json',
                'lessons/tests/fixtures/default_administrator.json'
               ]

    def setUp(self):
        self.url = reverse('manage_admins')
        self.user2 = Administrator.objects.get(email='bob_green@email.com')
        self.user = Director.objects.get(email='alex_green@email.org')

    def test_admin_manage_url(self):
        self.assertEqual(self.url,'/director/manage_admins')
    
    def test_admin_manage_view(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_admins.html')
        self.assertContains(response, 'Create a new Administrator Account')
        self.assertContains(response, 'Manage Administrators')

    def test_admin_manage_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/log_in/?next=/director/manage_admins')

    def test_admin_manage_view_not_director(self):
        self.login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/administrator/lessons')
