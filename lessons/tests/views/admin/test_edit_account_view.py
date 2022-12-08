"""Tests of the edit account view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Director, Student
from lessons.tests.helper import LogInTester
from lessons.forms import AccountForm

class EditAccountViewTestCase(TestCase, LogInTester):
    """Tests of the edit account view."""

    fixtures = [
                'lessons/tests/fixtures/default_user.json',
                'lessons/tests/fixtures/default_director.json',
                'lessons/tests/fixtures/default_administrator.json',
                'lessons/tests/fixtures/other_students_2.json'
               ]

    def setUp(self):
        self.url = reverse('edit_account' , args=[1])
        self.user = Director.objects.get(email='alex_green@email.org')

        self.form_input = {
            'first_name': 'David',
            'last_name': 'Fest',
            'email': 'devfest@example.org',
            "role": "Administrator"
        }

    def test_admin_manage_url(self):
        self.assertEqual(self.url,'/edit_account/1')
    
    def test_admin_manage_view(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard/edit_account.html')
        self.assertContains(response, 'Edit account')
        self.assertContains(response, 'First name:')
        self.assertContains(response, 'Last name:')
        self.assertContains(response, 'Email:')
        self.assertContains(response, 'Role:')
        self.assertContains(response, 'Update')
        self.assertContains(response, 'Back')
        form = response.context['form']
        self.assertTrue(isinstance(form, AccountForm))
        self.assertFalse(form.is_bound)
    
    def test_admin_manage_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/log_in/?next=/edit_account/1')

    def test_get_admin_manage_redirects_when_not_director_or_administrator(self):
        self.user = Student.objects.get(id=3)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_dashboard/student_requests.html')

    def test_get_admin_manage_update_parses_form_is_instance_of_correct_account(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        account = response.context["account"]
        self.assertTrue(isinstance(form, AccountForm))
        self.assertEqual(form.instance, account)
