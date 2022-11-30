from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import faker.providers
from lessons.models import User, Student, Teacher, Administrator, Lesson, Invoice, Instrument, Request
import random
from django.conf import settings
import datetime


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
        num_reqs = random.randint(1, 5)

        if req_made:
            for _ in range(num_reqs):
                time_availability = fake.future_datetime().time()
                day_availability = random.choice(settings.DAYS_OF_THE_WEEK)[0]
                duration = random.choice(settings.LESSON_DURATIONS)[0]

                pref_teacher = Teacher.objects.get(id=random.choice(teacher_ids))

                student = Student.objects.get(id=each)

                chosen_inst = Instrument.objects.get(id=random.choice(instruments))

                approved = bool(random.getrandbits(1))

                les_count = random.randint(1, 5)

                Request.objects.create(time_availability=time_availability,
                                       day_availability=day_availability,
                                       lesson_count=les_count,
                                       lesson_duration=duration,
                                       preferred_teacher=pref_teacher,
                                       instrument=chosen_inst,
                                       student=student,
                                       is_approved=approved)


def populate_lessons():
    teachers = list(Teacher.objects.all())
    instruments = list(Instrument.objects.all())
    for request in Request.objects.all():
        if request.is_approved:
            pref_teacher = random.choice(teachers)
            instrument = random.choice(instruments)
            student = Student.objects.get(email=request.student)
            datetime_obj = datetime.datetime.combine(datetime.datetime.now(), request.time_availability)
            Lesson.objects.create(time=datetime_obj,
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
