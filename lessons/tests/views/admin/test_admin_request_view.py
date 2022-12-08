"""Tests of the admin request view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Director, Request, Term, Lesson
from lessons.tests.helper import LogInTester
from datetime import time

class AdminRequestViewTestCase(TestCase, LogInTester):
    """Tests of the admin request view."""

    fixtures = [
        'lessons/tests/fixtures/other_directors.json',
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/other_requests.json',
        'lessons/tests/fixtures/default_term.json',
        'lessons/tests/fixtures/other_teachers.json',
    ]

    def setUp(self):
        self.request = Request.objects.get(pk=2)
        self.url = reverse('admin_request', kwargs={"request_id": 2})
        self.user = Director.objects.get(email='alex_green@email.org')

        self.form_input = {
            "time_availability": time(hour=13, minute=30),
            "day_availability": 3,
            "lesson_interval": 2,
            "lesson_count": 3,
            "lesson_duration": 45,
            "instrument": 2,
            "term": 2,
            "teacher": 3
        }

    def test_admin_request_url(self):
        self.assertEqual(self.url,'/administrator/requests/2')

    def test_admin_request_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/log_in/?next=/administrator/requests/2')

    def test_get_admin_request_view(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'admin_dashboard/admin_request.html')

    def test_post_admin_request_view_successful(self):
        self.login(self.user)
        before_count = Lesson.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Lesson.objects.count()
        redirect_url = reverse('admin_unapproved_requests')
        self.assertEqual(before_count, after_count - self.form_input["lesson_count"])
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_dashboard/admin_unapproved_requests.html')

    def test_post_admin_request_view_unsuccessful(self):
        self.login(self.user)
        before_count = Lesson.objects.count()
        self.form_input["lesson_count"] = 2 
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Lesson.objects.count()
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(before_count, after_count)
        self.assertTemplateUsed(response, 'admin_dashboard/admin_request.html')