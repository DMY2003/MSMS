"""Tests of the admin request delete view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Director, Request, Administrator, Student
from lessons.tests.helper import LogInTester


class AdminRequestDeleteViewTestCase(TestCase, LogInTester):
    """Tests of the admin request delete view."""

    fixtures = [
        'lessons/tests/fixtures/other_directors.json',
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/other_requests.json',
    ]

    def setUp(self):
        self.url = reverse('admin_request_delete', kwargs={"request_id": 2})
        self.user = Director.objects.get(email='alex_green@email.org')
    
    def test_admin_request_delete_view(self):
        self.login(self.user)
        before_count = Request.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Request.objects.count()
        response_url = reverse('admin_unapproved_requests')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_unapproved_requests.html')
        self.assertEqual(before_count - 1, after_count)

    def test_term_delete_view_with_nonexistent_term(self):
        self.login(self.user)
        url = reverse('admin_request_delete', kwargs={"request_id": 10})
        before_count = Request.objects.count()
        response = self.client.post(url, follow=True)
        after_count = Request.objects.count()
        response_url = reverse('admin_unapproved_requests')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_unapproved_requests.html')
        self.assertEqual(before_count, after_count)

    # def test_redirect_home_if_not_logged_in(self):
    #     self.log_out()
    #     response = self.client.post(self.url, follow=True)
    #     response_url = reverse('home')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)