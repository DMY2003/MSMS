"""Tests of the student requests view."""
from django.test import TestCase
from django.urls import reverse

class StudentRequestsViewTestCase(TestCase):
    """Tests of the student requests view."""

    def setUp(self):
        self.url = reverse('student_requests')

    def test_student_requests_url(self):
        self.assertEqual(self.url,'/requests/')

    # def test_get_student_requests(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'student_requests.html')