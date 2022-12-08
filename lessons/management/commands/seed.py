from sys import stdout
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User, Student, Teacher, Administrator, Lesson, Invoice, Instrument, Request, Director, Term, \
    Child, Transaction
import random
from django.conf import settings
from datetime import datetime, timedelta


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        self.populate_admin()
        self.populate_teacher()
        self.populate_student()
        self.create_test_accs()
        self.populate_instruments()
        self.populate_terms()
        self.populate_requests()
        self.populate_lessons()
        # self.populate_invoices()
        self.create_superuser()
        self.stdout.write('done.')

    def create_test_accs(self):
        self.stdout.write('creating test accounts...')
        # Student
        student_fname = "John"
        student_lname = "Doe"
        email = "john.doe@example.org"
        balance = self.faker.random_int(min=0, max=500)
        password = "Password123"
        last_lgn = self.faker.past_datetime()

        student = Student.objects.create(first_name=student_fname,
                                         last_name=student_lname,
                                         email=email,
                                         username=email,
                                         balance=balance,
                                         password=make_password(password, salt=None, hasher='default'),
                                         last_login=last_lgn,
                                         role="Student")

        self.populate_transactions(student)

        num_children = self.faker.random_int(min=1, max=3)

        for _ in range(num_children):
            self.add_new_child("joe", student)

        # Admin
        admin_fname = "Petra"
        admin_lname = "Pickles"
        email = "petra.pickles@example.org"
        password = "Password123"
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
        # Director
        dir_fname = "Marty"
        dir_lname = "Major"
        email = "marty.major@example.org"
        password = "Password123"
        last_lgn = self.faker.past_datetime()
        Director.objects.create(first_name=dir_fname,
                                last_name=dir_lname,
                                email=email,
                                username=email,
                                password=make_password(password, salt=None, hasher='default'),
                                last_login=last_lgn,
                                is_staff=1,
                                is_superuser=1,
                                role="Director")

    def create_superuser(self):
        self.stdout.write('creating superuser...')

        user = User.objects.create_user(
            username="admin",
            email="admin@example.org",
            password="Password123",
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.role = "Administrator"
        user.save()

    def populate_terms(self):
        self.stdout.write('seeding terms...')

        term_lengths = [8, 10, 12]
        holiday = [1, 2]
        current_date = datetime.today() - timedelta(weeks=random.randrange(3, 6))

        for _ in range(random.randrange(3, 5)):
            end_date = current_date + timedelta(weeks=random.choice(term_lengths))

            Term.objects.create(
                start_date=current_date,
                end_date=end_date,
            )

            current_date = end_date + timedelta(weeks=random.choice(holiday))

    def populate_admin(self):
        self.stdout.write('seeding admin...')
        for i in range(10):
            admin_fname = self.faker.first_name()
            admin_lname = self.faker.last_name()
            email = str(i) + self.faker.free_email()
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

        for i in range(len(teacher_list)):
            each = teacher_list[i]
            email = str(i) + self.faker.free_email()
            Teacher.objects.create(first_name=each[0],
                                   last_name=each[1],
                                   email=email,
                                   is_staff=1,
                                   role="Teacher")

    def add_new_child(self, i, parent):
        child_fname = self.faker.first_name()
        child_lname = self.faker.last_name()
        email = str(i) + "Child_" + self.faker.free_email()

        Child.objects.create(first_name=child_fname,
                             last_name=child_lname,
                             parent=parent,
                             email=email,
                             role="Student")

    def populate_transactions(self, student):
        notes = ["Book Lesson", "Penalty", "Instrument hire"]
        amount = self.faker.random_int(min=0, max=student.balance)
        diff = "-£" + str(amount)
        new_balance = student.balance - amount

        Transaction.objects.create(student=student,
                                   note=random.choice(notes),
                                   change=diff,
                                   old_balance=student.balance,
                                   new_balance=new_balance
                                   )
        student.balance = new_balance
        student.save()

    def populate_student(self):
        self.stdout.write('seeding student...')
        for i in range(25):
            student_fname = self.faker.first_name()
            student_lname = self.faker.last_name()
            email = str(i) + self.faker.free_email()
            balance = self.faker.random_int(min=0, max=500)
            password = self.faker.password(length=12)
            last_lgn = self.faker.past_datetime()

            student = Student.objects.create(first_name=student_fname,
                                             last_name=student_lname,
                                             email=email,
                                             username=email,
                                             balance=balance,
                                             password=make_password(password, salt=None, hasher='default'),
                                             last_login=last_lgn,
                                             role="Student")

            num_children = self.faker.random_int(min=0, max=2)

            for _ in range(num_children):
                self.add_new_child(i, student)

            self.populate_transactions(student)

    def populate_instruments(self):
        self.stdout.write('seeding instruments...')
        instruments = {"Guitar": 50,
                       "Ukulele": 50,
                       "Violin": 50,
                       "Recorder": 50,
                       "Piano": 50,
                       "Triangle": 50}

        for key, value in instruments.items():
            Instrument.objects.create(name=key, base_price=value)

    def populate_requests(self):
        self.stdout.write('seeding requests...')
        students = list(Student.objects.all())
        instruments = list(Instrument.objects.all())

        for student in students:
            if student.email == "john.doe@example.org":
                approval = 1
            else:
                approval = random.getrandbits(1)
            for _ in range(self.faker.random_int(min=1, max=3)):
                time_availability = self.faker.future_datetime().time()
                day_availability = random.choice(settings.DAYS_OF_THE_WEEK)[0]
                duration = random.choice(settings.LESSON_DURATIONS)[0]
                preferred_teacher = self.faker.first_name() + " " + self.faker.last_name()
                les_count = 3 + random.randrange(4)

                Request.objects.create(time_availability=time_availability,
                                       day_availability=day_availability,
                                       lesson_count=les_count,
                                       lesson_duration=duration,
                                       lesson_interval=1,
                                       preferred_teacher=preferred_teacher,
                                       instrument=random.choice(instruments),
                                       student=random.choice(students),
                                       is_approved=approval)



    def populate_lessons(self):
        self.stdout.write('seeding lessons...')
        teacher_list = list(Teacher.objects.all())
        term_list = list(Term.objects.all())

        for request in Request.objects.all():
            if request.is_approved:
                pref_teacher = random.choice(teacher_list)
                request.generate_lessons(
                    pref_teacher,
                    random.choice(term_list)
                )

    def populate_invoices(self):
        self.stdout.write('seeding invoices...')
        lesson_ids = Lesson.objects.values_list('id', flat=True).distinct()
        for each in lesson_ids:
            price = random.randint(50, 150)
            paid = bool(random.getrandbits(1))
            lesson = Lesson.objects.get(id=each)

            Invoice.objects.create(price=price, paid=paid, lesson=lesson)
