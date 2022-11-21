from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import faker.providers
from lessons.models import User, Student, Teacher, Administrator, Invoice, Request
import random

teachers = ["John Doe",
            "Jane Doe",
            "Sarah Palmer",
            "Jessica Swift"]

instruments = ["Guitar",
               "Ukelele",
               "Violin",
               "Recorder",
               "Piano",
               "Triangle"]


class Provider(faker.providers.BaseProvider):
    def teachers(self):
        return self.random_element(teachers)

    def instrument(self):
        return self.random_element(instruments)


def populate_student(fake):
    for _ in range(100):
        student_fname = fake.first_name()
        student_lname = fake.last_name()
        email = fake.free_email()
        balance = fake.random_int(min=0, max=500)
        password = fake.password(length=12)
        last_lgn = fake.past_datetime()

        Student.objects.create(first_name=student_fname,
                               last_name=student_lname,
                               email=email,
                               balance=balance,
                               password=password,
                               last_login=last_lgn)


def populate_teacher(fake):
    for _ in range(20):
        teacher_fname = fake.first_name()
        teacher_lname = fake.last_name()
        email = fake.free_email()
        Teacher.objects.create(first_name=teacher_fname,
                               last_name=teacher_lname,
                               email=email,
                               is_staff=1)


def populate_admin(fake):
    for _ in range(10):
        admin_fname = fake.first_name()
        admin_lname = fake.last_name()
        email = fake.free_email()
        password = fake.password(length=12)
        last_lgn = fake.past_datetime()
        Administrator.objects.create(first_name=admin_fname,
                                     last_name=admin_lname,
                                     email=email,
                                     password=password,
                                     last_login=last_lgn,
                                     is_staff=1,
                                     is_superuser=1)


# def populate_requests(fake):
#     for _ in range(20):
#         avail = fake.future_datetime()
#         count = fake.random_int(min=0, max=100)
#         duration = fake.random_int(min=0, max=240)
#         t_name = fake.teachers()
#         instrument = fake.instrument()
#         student_fname = fake.first_name()
#         student_lname = fake.last_name()
#         student = student_fname + " " + student_lname
#         is_approved = fake.boolean()
#
#         Request.objects.create(student_availability=avail,
#                                lesson_count=count,
#                                lesson_duration=duration,
#                                preferred_teacher=t_name,
#                                instrument=instrument,
#                                student=student,
#                                is_approved=is_approved)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        fake = Faker("en_GB")
        fake.add_provider(Provider)

        self.stdout.write('seeding admin...')
        populate_admin(fake)
        self.stdout.write('seeding teacher...')
        populate_teacher(fake)
        self.stdout.write('seeding student...')
        populate_student(fake)

        self.stdout.write('done.')
