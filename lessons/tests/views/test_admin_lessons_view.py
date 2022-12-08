"""Tests of the admin lessons view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Administrator, Lesson, Student
from lessons.tests.helper import reverse_with_next

class AdminLessonsViewTestCase(TestCase):
    """Tests of the admin lessons view."""

    fixtures = [
        'lessons/tests/fixtures/default_administrator.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/other_teachers.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/other_admin_lessons.json',
        ]

    def setUp(self):
        self.user = Administrator.objects.get(id=1)
        self.url = reverse('admin_lessons')

    def test_admin_lessons_url(self):
        self.assertEqual(self.url,'/administrator/lessons')

    def test_get_admin_lessons(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_lessons.html')

    def test_admin_lessons_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_admin_lessons_redirects_when_not_director_or_administrator(self):
        self.user = Student.objects.get(id=2)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_requests.html')

    def test_get_admin_lesson_parses_correct_lesson_queryset(self):
        self.user = Administrator.objects.get(id=1)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        lessons = response.context["lessons"]
        self.assertEqual(len(lessons),8)

    def test_get_admin_lessons_returns_queryset_with_correct_student_lessons(self):
        self.client.login(email=self.user.email, password='Password123')
        data = {"name_search":"Jane Doe"}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        lessons = response.context["lessons"]
        self.assertEqual(len(lessons),4)
