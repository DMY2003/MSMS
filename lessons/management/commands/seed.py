from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import faker.providers
from lessons.models import User, Student, Lesson, Instrument, Invoice, Request
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

def populate_users(fake):
    for _ in range(20):
        student_fname = fake.first_name()
        student_lname = fake.last_name()
        email = fake.free_email()

        User.objects.create(first_name=student_fname, last_name=student_lname, email=email)

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

        populate_users(fake)

        self.stdout.write('done.')
