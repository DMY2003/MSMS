"""Tests of the term delete view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Director, Term
from lessons.tests.helper import LogInTester


class TermDeleteViewTestCase(TestCase, LogInTester):
    """Tests of the term delete view."""

    fixtures = [
        'lessons/tests/fixtures/default_director.json',
        'lessons/tests/fixtures/default_term.json'
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
        self.assertTemplateUsed(response, 'term_create.html')
        self.assertEqual(before_count - 1, after_count)

    # def test_admin_manage_view_not_logged_in(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/log_in/?next=/director/manage_admins')

    # def test_admin_manage_view_not_director(self):
    #     self.user2 = Administrator.objects.get(email='"bob_green@email.com')
    #     self.login(self.user2)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/')