"""Tests of the remove account view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Director, Administrator, Student
from lessons.tests.helper import LogInTester

class RemoveAccountViewTestCase(TestCase, LogInTester):
    """Tests of the student requests view."""

    fixtures = [
                'lessons/tests/fixtures/default_director.json',
                'lessons/tests/fixtures/default_administrator.json',
                'lessons/tests/fixtures/other_students_2.json'
               ]

    def setUp(self):
        self.url = reverse('manage_user_delete', args=[1])
        self.url2 = reverse('manage_user_delete', args=[3])
        
        self.user2 = Administrator.objects.get(email='bob_green@email.com')
        self.user = Director.objects.get(email='alex_green@email.org')
        self.user3 = Student.objects.get(email='georgedoe@example.org')

    def test_remove_account_url(self):
        self.assertEqual(self.url,'/administrator/delete_user/1')

    def test_remove_account_successfully_as_director(self):
        self.login(self.user)
        countBefore = User.objects.all().count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        countAfter = User.objects.all().count()
        self.assertEqual(countAfter, countBefore-1)

    def test_remove_account_successfully_as_administrator(self):
        self.login(self.user2)
        countBefore = User.objects.all().count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        countAfter = User.objects.all().count()
        self.assertEqual(countAfter, countBefore-1)

    def test_remove_account_successfully_a_student_as_administrator(self):
        self.login(self.user)
        countBefore = User.objects.all().count()
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 302)
        countAfter = User.objects.all().count()
        self.assertEqual(countAfter, countBefore-1)