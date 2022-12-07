from django.core.management.base import BaseCommand, CommandError
from lessons.models import User, Student, Teacher, Administrator, Lesson, Invoice, Instrument, Request, Term

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Unseeding data...')
        User.objects.all().delete()
        Student.objects.all().delete()
        Teacher.objects.all().delete()
        Administrator.objects.all().delete()
        Lesson.objects.all().delete()
        Invoice.objects.all().delete()
        Instrument.objects.all().delete()
        Request.objects.all().delete()
        Term.objects.all().delete()
        self.stdout.write('Complete')
