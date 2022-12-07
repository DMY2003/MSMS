"""Tests of the student request delete view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Request
from lessons.tests.helper import reverse_with_next

class StudentRequestDeleteViewTestCase(TestCase):
    """Tests of the student request delete view."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/other_requests.json',
        ]

    def setUp(self):
        self.user = Student.objects.get(email='johndoe@example.org')
        self.url = reverse('student_request_delete', kwargs={'request_id': 6666})
    
    def test_student_request_delele_url(self):
        self.assertEqual(self.url,'/delete_request/6666')

    def test_get_student_request_delete(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_student_request_delete_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_student_reqeust_delete_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        self.url = reverse('student_request_delete', kwargs={'request_id': 6667})
        request = Request.objects.get(id=6667)
        self.assertTrue(request)
        request_size_before = Request.objects.count()
        response = self.client.get(self.url)
        request_size_after = Request.objects.count()
        self.assertEqual(request_size_before, request_size_after+1)
        request = Request.objects.filter(id=6667)
        self.assertEqual(len(request),0)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)