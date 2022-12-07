"""Tests of the admin lesson view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Administrator, Lesson, Student, Teacher, Instrument
from lessons.tests.helper import reverse_with_next
from lessons.forms import AdminLessonForm
import datetime

class AdminLessonViewTestCase(TestCase):
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
        self.url = reverse('admin_lesson', kwargs={'lesson_id': 10})
        self.form_input = {
            "date": datetime.datetime(year=2022,month=12,day=5,hour=12,minute=30,second=00),
            "duration": 45,
            "teacher": 3,
            'instrument': 1
        }

    def test_admin_lesson_url(self):
        self.assertEqual(self.url,'/administrator/lessons/10')

    def test_get_admin_lesson(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_lesson.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AdminLessonForm))

    def test_admin_lesson_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_admin_lesson_redirects_when_not_director_or_administrator(self):
        self.user = Student.objects.get(id=2)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('student_requests')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_requests.html')

    def test_get_admin_lesson_returns_correct_lesson(self):
        self.user = Administrator.objects.get(id=1)
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        lesson = response.context["lesson"]
        self.assertEqual(lesson.id,10)

    def test_get_admin_form_is_instance_of_correct_lesson(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        lesson = response.context["lesson"]
        self.assertTrue(isinstance(form, AdminLessonForm))
        self.assertEqual(form.instance, lesson)

    def test_student_reqeust_update_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        lesson = Lesson.objects.get(id=10)

        self.assertTrue(lesson)
        self.assertEqual(lesson.id, 10)
        self.assertEqual(lesson.duration, 60)

        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_lesson.html')

        lesson = Lesson.objects.get(id=10)
        self.assertEqual(lesson.id, 10)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "The lesson was successfully updated!")
        self.assertEqual(lesson.duration, 45)

    def test_student_admin_lesson_unsuccessful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.form_input["instrument"] = "Guitar"

        lesson = Lesson.objects.get(id=10)

        self.assertTrue(lesson)
        self.assertEqual(lesson.instrument.name, "Piano")
        self.assertEqual(lesson.id, 10)

        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_lesson.html')

        lesson = Lesson.objects.get(id=10)
        self.assertEqual(lesson.instrument.name, "Piano")