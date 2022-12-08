"""Tests of the admin lesson delete view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Administrator, Request, Student, Lesson
from lessons.tests.helper import reverse_with_next

class AdminLessonDeleteViewTestCase(TestCase):
    """Tests of the student request delete view."""

    fixtures = [
        'lessons/tests/fixtures/other_students.json',
         'lessons/tests/fixtures/other_teachers.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_administrator.json',
        'lessons/tests/fixtures/other_admin_lessons.json',
        ]

    def setUp(self):
        self.user = Administrator.objects.get(id=1)
        self.url = reverse('admin_lesson_delete', kwargs={'lesson_id': 15})
    
    def test_student_request_delele_url(self):
        self.assertEqual(self.url,'/administrator/delete_lesson/15')

    def test_get_student_request_delete(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('admin_lessons')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_student_request_delete_redirects_when_not_logged_in(self):
        self.url = reverse('admin_lesson_delete', kwargs={'lesson_id': 16})
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_admin_lesson_delete_redirects_when_not_director_or_administrator(self):
        self.user = Student.objects.get(id=2)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_dashboard/student_requests.html')

    def test_admin_lesson_delete_delete_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        self.url = reverse('admin_lesson_delete', kwargs={'lesson_id': 17})
        lesson = Lesson.objects.get(id=17)
        self.assertTrue(lesson)
        lesson_size_before = Lesson.objects.count()
        response = self.client.get(self.url)
        lesson_size_after = Lesson.objects.count()
        self.assertEqual(lesson_size_before, lesson_size_after+1)
        lesson = Lesson.objects.filter(id=17)
        self.assertEqual(len(lesson),0)
        redirect_url = reverse('admin_lessons')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    