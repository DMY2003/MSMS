"""Tests of the edit account view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Director

class EditAccountViewTestCase(TestCase):
    """Tests of the edit account view."""

    fixtures = ['lessons/tests/fixtures/default_director.json']

    def setUp(self):
        self.url = reverse('edit_account' , args=[1])
        self.user = Director.objects.get(email='alex_green@email.org')

    def test_admin_manage_url(self):
        self.assertEqual(self.url,'/edit_account/1')