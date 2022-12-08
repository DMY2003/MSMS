"""Unit tests of the Upate balance form."""
from django import forms
from django.test import TestCase
from lessons.forms import UpdateBalance
from lessons.models import Instrument,Invoice, Student, Transaction
import datetime


class UpdateBalanceFormTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/other_students.json',
        'lessons/tests/fixtures/default_instrument.json',
        'lessons/tests/fixtures/default_request.json',
        ]

    def setUp(self):
        self.user = Student.objects.get(id=2)
        self.form_input = {
            'note': "Cose of first lessons",
            'balance': 10,
        }
    
    # default test
    def test_valid_update_balance_form(self):
        form = UpdateBalance(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_update_balance_form_has_necessary_fields(self):
        form = UpdateBalance(user=self.user)
        self.assertIn('note', form.fields)
        note_field = form.fields['note']
        self.assertTrue(isinstance(note_field, forms.CharField))
        self.assertIn('balance', form.fields)
        balance_field = form.fields['balance']
        self.assertTrue(isinstance(balance_field, forms.IntegerField))
        self.assertIn('student', form.fields)
        student_field= form.fields['student']
        self.assertTrue(isinstance(student_field, forms.ModelChoiceField))

    #note tests
    def test_note_can_be_blank(self):
        self.form_input['note'] = ''
        form = UpdateBalance(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_note_can_take_up_to_25_characters(self):
        self.form_input['note'] = 'x'*25
        form = UpdateBalance(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_note_must_not_take_more_than_25_characters(self):
        self.form_input['note'] = 'x'*26
        form = UpdateBalance(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())

    #balance tests
    def test_balance_must_be_a_number(self):
        self.form_input["balance"] = "forty"
        form = UpdateBalance(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
        self.form_input["balance"] = "40"
        form = UpdateBalance(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())
        self.form_input["balance"] = 40
        form = UpdateBalance(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_update_balance_form_must_save_correctly(self):
        form = UpdateBalance(data=self.form_input, user=self.user)
        before_transactions_count = Transaction.objects.count()
        if form.is_valid():
            form.save()
        self.user = Student.objects.get(id=2)
        after_transactions_count = Transaction.objects.count()
        self.assertEqual(before_transactions_count+1, after_transactions_count)

    def test_update_balance_form_must_subracts_balance_correctly(self):
        self.form_input["Subtract"] = ""
        form = UpdateBalance(data=self.form_input, user=self.user)
        before_transactions_count = Transaction.objects.count()
        before_balance = self.user.balance
        if form.is_valid():
            form.save()
        self.user = Student.objects.get(id=2)
        after_balance = self.user.balance
        after_transactions_count = Transaction.objects.count()
        self.assertEqual(before_balance, after_balance+10)
        self.assertEqual(before_transactions_count+1, after_transactions_count)


    def test_update_balance_form_must_adds_balance_correctly(self):
        self.form_input["Add"] = ""
        form = UpdateBalance(data=self.form_input, user=self.user)
        before_transactions_count = Transaction.objects.count()
        before_balance = self.user.balance
        if form.is_valid():
            form.save()
        self.user = Student.objects.get(id=2)
        after_balance = self.user.balance
        after_transactions_count = Transaction.objects.count()
        self.assertEqual(before_balance, after_balance-10)
        self.assertEqual(before_transactions_count+1, after_transactions_count)

    def test_update_balance_form_must_changes_balance_correctly(self):
        self.form_input["Change"] = ""
        form = UpdateBalance(data=self.form_input, user=self.user)
        before_transactions_count = Transaction.objects.count()
        if form.is_valid():
            form.save()
        self.user = Student.objects.get(id=2)
        after_balance = self.user.balance
        after_transactions_count = Transaction.objects.count()
        self.assertEqual(after_balance,10)
        self.assertEqual(before_transactions_count+1, after_transactions_count) 
