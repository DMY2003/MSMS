from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import Student, Teacher, Administrator, Lesson, Invoice, Instrument, Request
import random


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        self.populate_admin()
        self.populate_teacher()
        self.populate_student()
        self.populate_instruments()
        self.populate_requests()
        self.populate_lessons()
        self.populate_invoices()
        self.stdout.write('done.')

    def populate_admin(self):
        self.stdout.write('seeding admin...')
        for _ in range(3):
            admin_fname = self.faker.first_name()
            admin_lname = self.faker.last_name()
            email = self.faker.free_email()
            password = self.faker.password(length=12)
            last_lgn = self.faker.past_datetime()
            Administrator.objects.create(first_name=admin_fname,
                                         last_name=admin_lname,
                                         email=email,
                                         username=email,
                                         password=make_password(password, salt=None, hasher='default'),
                                         last_login=last_lgn,
                                         is_staff=1,
                                         is_superuser=1,
                                         role="Administrator")

    def populate_teacher(self):
        self.stdout.write('seeding teacher...')
        teacher_list = [["Sarah", "Palmer"],
                        ["Jessica", "Swift"],
                        ["John", "Smith"]]

        for each in teacher_list:
            email = self.faker.free_email()
            Teacher.objects.create(first_name=each[0],
                                   last_name=each[1],
                                   email=email,
                                   is_staff=1,
                                   role="Teacher")

    def populate_student(self):
        self.stdout.write('seeding student...')
        for _ in range(100):
            student_fname = self.faker.first_name()
            student_lname = self.faker.last_name()
            email = self.faker.free_email()
            balance = self.faker.random_int(min=0, max=500)
            password = self.faker.password(length=12)
            last_lgn = self.faker.past_datetime()

            Student.objects.create(first_name=student_fname,
                                   last_name=student_lname,
                                   email=email,
                                   username=email,
                                   balance=balance,
                                   password=make_password(password, salt=None, hasher='default'),
                                   last_login=last_lgn,
                                   role="Student")

    def populate_instruments(self):
        self.stdout.write('seeding instruments...')
        instruments = ["Guitar",
                       "Ukulele",
                       "Violin",
                       "Recorder",
                       "Piano",
                       "Triangle"]

        for each in instruments:
            Instrument.objects.create(name=each)

    def populate_invoices(self):
        self.stdout.write('seeding invoices...')
        lesson_ids = Lesson.objects.values_list('id', flat=True).distinct()

        for each in lesson_ids:
            price = random.randint(50, 150)
            paid = bool(random.getrandbits(1))
            lesson = Lesson.objects.get(id=each)

            Invoice.objects.create(price=price, paid=paid, lesson=lesson)

    def populate_requests(self):
        self.stdout.write('seeding requests...')
        student_ids = Student.objects.values_list('id', flat=True).distinct()
        teacher_ids = Teacher.objects.values_list('id', flat=True).distinct()
        instruments = Instrument.objects.values_list('id', flat=True).distinct()

        for each in student_ids:
            req_made = bool(random.getrandbits(1))

            if req_made:
                time = self.faker.time_object()
                day = self.faker.day_of_week()
                duration = random.choice(range(30, 240, 30))
                pref_teacher = Teacher.objects.get(id=random.choice(teacher_ids))
                student = Student.objects.get(id=each)
                chosen_inst = Instrument.objects.get(id=random.choice(instruments))
                approved = bool(random.getrandbits(1))
                les_count = random.randint(1, 5)
                Request.objects.create(time_availability=time,
                                       day_availability=day,
                                       lesson_count=les_count,
                                       lesson_duration=duration,
                                       lesson_interval=random.randint(1, 2),
                                       preferred_teacher=pref_teacher,
                                       instrument=chosen_inst,
                                       student=student,
                                       is_approved=approved)

    def populate_lessons(self):
        self.stdout.write('seeding lessons...')
        for request in Request.objects.all():
            if request.is_approved:
                pref_teacher = Teacher.objects.get(email=request.preferred_teacher)
                student = Student.objects.get(email=request.student)
                Lesson.objects.create(time=request.time_availability,
                                      day=request.day_availability,
                                      teacher=pref_teacher,
                                      student=student)
