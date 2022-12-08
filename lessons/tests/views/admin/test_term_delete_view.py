"""Tests of the term delete view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Director, Term, Student
from lessons.tests.helper import LogInTester


class TermDeleteViewTestCase(TestCase, LogInTester):
    """Tests of the term delete view."""

    fixtures = [
        'lessons/tests/fixtures/default_director.json',
        'lessons/tests/fixtures/default_term.json',
        'lessons/tests/fixtures/other_students_2.json',
    ]

    def setUp(self):
        self.url = reverse('term_delete', kwargs={"term_id": 1})
        self.user = Director.objects.get(email='alex_green@email.org')
    
    def test_term_delete_view(self):
        self.login(self.user)
        before_count = Term.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Term.objects.count()
        response_url = reverse('term_create')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_dashboard/term_create.html')
        self.assertEqual(before_count - 1, after_count)

    def test_term_delete_view_with_nonexistent_term(self):
        self.login(self.user)
        url = reverse('term_delete', kwargs={"term_id": 10})
        before_count = Term.objects.count()
        response = self.client.post(url, follow=True)
        after_count = Term.objects.count()
        response_url = reverse('term_create')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_dashboard/term_create.html')
        self.assertEqual(before_count, after_count)

    # def test_redirect_home_if_not_logged_in(self):
    #     self.log_out()
    #     response = self.client.post(self.url, follow=True)
    #     response_url = reverse('home')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_get_term_create_redirects_when_not_director_or_administrator(self):
        self.user = Student.objects.get(id=3)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_dashboard/student_requests.html')