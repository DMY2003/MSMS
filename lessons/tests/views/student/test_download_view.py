from django.test import TestCase
from django.urls import reverse
from lessons.pdf_generator import generate_invoice_PDF
from lessons.models import Invoice, Lesson, Request


# class TestDownloadView(TestCase):
#     fixtures = [
#         'lessons/tests/fixtures/default_student.json',
#         'lessons/tests/fixtures/default_instrument.json',
#         'lessons/tests/fixtures/default_teacher.json',
#         'lessons/tests/fixtures/default_request.json',
#         'lessons/tests/fixtures/default_lesson.json',
#         'lessons/tests/fixtures/default_invoice.json',
#     ]
#
#     def setUp(self):
#         self.request = Request.objects.get(id=1)
#         self.lesson = Lesson.objects.get(id=1)
#         self.invoice = Invoice.objects.get(id=1)
#
#         self.file_name = generate_invoice_PDF(self.invoice.id, self.lesson.student, self.lesson.teacher,
#                                               self.lesson.instrument.name, self.lesson.date, 50
#                                               )
#
#     def test_status_code(self):
#         path = self.file_name
#         url = reverse("download", args=[path])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_content_type(self):
#         path = self.file_name
#         response = self.client.get(reverse("download", args=[path]))
#         self.assertEqual(response.headers['Content-Type'], 'application/pdf')
