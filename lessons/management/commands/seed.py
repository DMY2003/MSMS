from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import faker.providers
from lessons.models import User, Student, Teacher, Administrator, Lesson, Invoice, Instrument, Request
import random


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
                               username=email,
                               balance=balance,
                               password=password,
                               last_login=last_lgn)


def populate_teacher(fake):
    teacher_list = [["Sarah", "Palmer"],
                    ["Jessica", "Swift"],
                    ["John", "Smith"]]

    for each in teacher_list:
        email = fake.free_email()
        Teacher.objects.create(first_name=each[0],
                               last_name=each[1],
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
                                     username=email,
                                     password=password,
                                     last_login=last_lgn,
                                     is_staff=1,
                                     is_superuser=1)


def populate_invoices():
    lesson_ids = Lesson.objects.values_list('id', flat=True).distinct()

    for each in lesson_ids:
        price = random.randint(50, 150)
        paid = bool(random.getrandbits(1))
        lesson = Lesson.objects.get(id=each)

        Invoice.objects.create(price=price, paid=paid, lesson=lesson)


def populate_requests(fake):
    student_ids = Student.objects.values_list('id', flat=True).distinct()
    teacher_ids = Teacher.objects.values_list('id', flat=True).distinct()
    instruments = Instrument.objects.values_list('id', flat=True).distinct()

    for each in student_ids:
        req_made = bool(random.getrandbits(1))

        if req_made:
            time = fake.time_object()

            day = fake.day_of_week()

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



def populate_lessons():
    for request in Request.objects.all():
        if request.is_approved:
            pref_teacher = Teacher.objects.get(email=request.preferred_teacher)
            student = Student.objects.get(email=request.student)
            Lesson.objects.create(time=request.time_availability,
                                  day=request.day_availability,
                                  teacher=pref_teacher,
                                  student=student)


def populate_instruments():
    instruments = ["Guitar",
                   "Ukulele",
                   "Violin",
                   "Recorder",
                   "Piano",
                   "Triangle"]

    for each in instruments:
        Instrument.objects.create(name=each)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        fake = Faker("en_GB")

        self.stdout.write('seeding admin...')
        populate_admin(fake)
        self.stdout.write('seeding teacher...')
        populate_teacher(fake)
        self.stdout.write('seeding student...')
        populate_student(fake)
        self.stdout.write('seeding instruments...')
        populate_instruments()
        self.stdout.write('seeding invoices...')
        populate_invoices()
        self.stdout.write('seeding requests...')
        populate_requests(fake)
        self.stdout.write('seeding lessons...')
        populate_lessons()
        self.stdout.write('done.')
