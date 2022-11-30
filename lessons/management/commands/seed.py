from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import faker.providers
from lessons.models import User, Student, Teacher, Administrator, Lesson, Invoice, Instrument, Request
import random
from django.conf import settings
import datetime


def populate_student(fake):
    for i in range(100):
        student_fname = fake.first_name()
        student_lname = fake.last_name()
        email = str(i) + fake.free_email()
        balance = fake.random_int(min=0, max=500)
        password = fake.password(length=12)
        last_lgn = fake.past_datetime()

        Student.objects.create(first_name=student_fname,
                               last_name=student_lname,
                               email=email,
                               username=email,
                               balance=balance,
                               password=make_password(password, salt=None, hasher='default'),
                               last_login=last_lgn,
                               role="Student")


def populate_teacher(fake):
    teacher_list = [["Sarah", "Palmer"],
                    ["Jessica", "Swift"],
                    ["John", "Smith"]]

    for each in teacher_list:
        email = fake.free_email()
        Teacher.objects.create(first_name=each[0],
                               last_name=each[1],
                               email=email,
                               is_staff=1,
                               role="Teacher")


def populate_admin(fake):
    for i in range(10):
        admin_fname = fake.first_name()
        admin_lname = fake.last_name()
        email = str(i) + fake.free_email()
        password = fake.password(length=12)
        last_lgn = fake.past_datetime()
        Administrator.objects.create(first_name=admin_fname,
                                     last_name=admin_lname,
                                     email=email,
                                     username=email,
                                     password=make_password(password, salt=None, hasher='default'),
                                     last_login=last_lgn,
                                     is_staff=1,
                                     is_superuser=1,
                                     role="Administrator")


def populate_invoices():
    lesson_ids = Lesson.objects.values_list('id', flat=True).distinct()

    for each in lesson_ids:
        price = random.randint(50, 150)
        paid = bool(random.getrandbits(1))
        lesson = Lesson.objects.get(id=each)

        Invoice.objects.create(price=price, paid=paid, lesson=lesson)


def populate_requests(fake):
    students = list(Student.objects.all())
    teachers = list(Teacher.objects.all())
    instruments = list(Instrument.objects.all())

    for each in students:
        req_made = bool(random.getrandbits(1))

        if req_made:
            for _ in range(5):
                time_availability = fake.future_datetime().time()
                day_availability = random.choice(settings.DAYS_OF_THE_WEEK)[0]
                duration = random.choice(settings.LESSON_DURATIONS)[0]
                preferred_teacher = fake.first_name() + " " + fake.last_name()
                les_count = 3 + random.randrange(4)

                Request.objects.create(time_availability=time_availability,
                                       day_availability=day_availability,
                                       lesson_count=les_count,
                                       lesson_duration=duration,
                                       preferred_teacher=preferred_teacher,
                                       instrument=random.choice(instruments),
                                       student=random.choice(students),
                                       is_approved=bool(random.getrandbits(1)))


def populate_lessons():
    teachers = list(Teacher.objects.all())
    instruments = list(Instrument.objects.all())
    for request in Request.objects.all():
        if request.is_approved:
            pref_teacher = random.choice(teachers)
            instrument = random.choice(instruments)
            student = Student.objects.get(email=request.student)
            datetime_obj = datetime.datetime.combine(datetime.datetime.now(), request.time_availability)
            Lesson.objects.create(date=datetime_obj,
                                  teacher=pref_teacher,
                                  student=student,
                                  instrument=instrument,
                                  duration=request.lesson_duration)


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
