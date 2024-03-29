"""Tests of the term create view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Director, Term
from lessons.tests.helper import LogInTester
from datetime import date


class TermCreateViewTestCase(TestCase, LogInTester):
    """Tests of the term create view."""

    fixtures = [
        'lessons/tests/fixtures/default_director.json',
    ]

    def setUp(self):
        self.url = reverse('term_create')
        self.form_input = {
            "start_date": date(2022, 12, 1),
            "end_date": date(2023, 1, 14),
        }
        self.user = Director.objects.get(email='alex_green@email.org')
    
    def test_term_create_view_successful(self):
        self.login(self.user)
        before_count = Term.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Term.objects.count()
        self.assertTemplateUsed(response, 'admin_dashboard/term_create.html')
        self.assertEqual(before_count + 1, after_count)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

    def test_term_create_view_get(self):
        self.login(self.user)
        before_count = Term.objects.count()
        response = self.client.get(self.url)
        after_count = Term.objects.count()
        self.assertTemplateUsed(response, 'admin_dashboard/term_create.html')
        self.assertEqual(before_count, after_count)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 0)

    def test_term_create_view_with_invalid_form(self):
        self.login(self.user)
        before_count = Term.objects.count()
        self.form_input["start_date"] = date(2023, 4, 1)
        response = self.client.post(self.url, self.form_input)
        after_count = Term.objects.count()
        self.assertTemplateUsed(response, 'admin_dashboard/term_create.html')
        self.assertEqual(before_count, after_count)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 0)
