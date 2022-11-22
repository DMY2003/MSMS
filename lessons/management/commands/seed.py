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


def populate_lessons(fake):
    teacher_ids = Teacher.objects.values_list('id', flat=True).distinct()
    student_ids = Student.objects.values_list('id', flat=True).distinct()

    i = 0
    while i < 50:
        student_id = Student.objects.get(id=random.choice(student_ids))
        teacher_id = Teacher.objects.get(id=random.choice(teacher_ids))
        num_lessons = random.randint(1, 6)

        for _ in range(num_lessons):
            time = fake.future_datetime()
            Lesson.objects.create(time=time, teacher=teacher_id, student=student_id)
            i = i + 1

def populate_invoices():
    lesson_ids = Lesson.objects.values_list('id', flat=True).distinct()

    for each in lesson_ids:
        price = random.randint(50, 150)
        paid = bool(random.getrandbits(1))
        lesson = Lesson.objects.get(id=each)

        Invoice.objects.create(price=price, paid=paid, lesson=lesson)

def populate_requests(fake):
    lesson_ids = Lesson.objects.values_list('id', flat=True).distinct()
    avail = fake.future_datetime()
    duration = random.choice(range(30, 240, 30))
    pref_teacher =
    instriment =


# student_availability = models.DateTimeField(blank=False)
#     lesson_count = models.IntegerField(blank=False)
#     lesson_duration = models.IntegerField(blank=False)
#     preferred_teacher = models.TextField()
#     instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=False)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
#     is_approved = models.BooleanField(default=False)
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
        self.stdout.write('seeding lessons...')
        populate_lessons(fake)
        self.stdout.write('seeding instruments...')
        populate_instruments()
        self.stdout.write('seeding invoices...')
        populate_invoices()
        self.stdout.write('done.')
