"""Tests of the student lessons view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Lesson
from lessons.tests.helper import reverse_with_next

class StudentLessonsViewTestCase(TestCase):
    """Tests of the student lessons view."""

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/other_teachers.json',
        'lessons/tests/fixtures/other_lessons.json',
        ]

    def setUp(self):
        self.user = Student.objects.get(id=1)
        self.url = reverse('student_lessons')

    def test_student_lessons_url(self):
        self.assertEqual(self.url,'/student/lessons')

    def test_get_student_lessons(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_lessons.html')

    def test_student_lessons_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_student_lessons_displays_lessons_belonging_to_correct_student(self):
        self.client.login(email=self.user.email, password='Password123')
        lesson1 = Lesson.objects.get(id=1234)
        lesson2 = Lesson.objects.get(id=2468)
        lesson3 = Lesson.objects.get(id=1357)
        response = self.client.get(self.url)
        self.assertContains(response, lesson1.id)
        self.assertContains(response, lesson2.id)
        self.assertNotContains(response, lesson3.id)

    def test_student_lessons_uses_correct_templates(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        templates = response.templates
        template_names = [template.name for template in templates]
        self.assertIn("base.html", template_names)
        self.assertIn("base_content.html", template_names)
        self.assertIn("partials/navbar.html", template_names)
        self.assertIn("partials/messages.html", template_names)
        self.assertIn("partials/student_lesson_card.html", template_names)
        self.assertIn('partials/pagination.html', template_names)

    def test_student_lessons_passes_correct_upcoming_lessons_queryset(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        upcoming_lessons = response.context["upcoming_lessons"]
        self.assertEqual(len(upcoming_lessons), 2)
        self.assertEqual(upcoming_lessons[0].id, 2468)
        self.assertEqual(upcoming_lessons[1].id, 8642)
    
    def test_student_request_passes_correct_previous_lessons_queryset(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        previous_lessons = response.context["previous_lessons"]
        self.assertEqual(len(previous_lessons), 1)
        self.assertEqual(previous_lessons[0].id, 1234)