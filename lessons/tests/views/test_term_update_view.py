"""Tests of the term update view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Director, Term
from lessons.tests.helper import LogInTester
from datetime import date


class TermUpdateViewTestCase(TestCase, LogInTester):
    """Tests of the term create view."""

    fixtures = [
        'lessons/tests/fixtures/default_director.json',
        'lessons/tests/fixtures/default_term.json',
    ]

    def setUp(self):
        self.url = reverse('term_update', kwargs={"term_id": 1})
        self.form_input = {
            "start_date": date(2023, 5, 1),
            "end_date": date(2023, 7, 14),
        }
        self.term = Term.objects.get(pk=1)
        self.user = Director.objects.get(email='alex_green@email.org')
    
    # def test_term_update_successful(self):
    #     self.login(self.user)
    #     before_count = Term.objects.count()
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     response_url = reverse('term_create')
    #     after_count = Term.objects.count()
    #     self.assertEqual(before_count, after_count)
    #     self.assertEqual(self.term.start_date, self.form_input["start_date"])
    #     self.assertEqual(self.term.end_date, self.form_input["end_date"])
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'term_create.html')
