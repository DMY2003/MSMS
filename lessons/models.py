from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import datetime
from django.conf import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=False, unique=False)
    first_name = models.CharField(max_length=50, blank=False, unique=False)
    last_name = models.CharField(max_length=50, blank=False, unique=False)
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=50, blank=False, unique=False, default="User")
    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        """Gets the full name of a user"""
        return "%s %s" % (self.first_name, self.last_name)


class Student(User):
    balance = models.IntegerField(default=0)


class Teacher(User):
    def __str__(self):
        return self.full_name


class Administrator(User):
    pass


class Director(User):
    pass


class Instrument(models.Model):
    name = models.CharField(max_length=30, blank=False)
    base_price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    date = models.DateTimeField(null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=False)
    duration = models.IntegerField(choices=settings.LESSON_DURATIONS)

    class Meta:
        ordering = ('date',)


def get_date_from_weekday(weekday, time):
    """Gets the date from the weekday"""
    today = datetime.date.today()
    today = datetime.datetime.combine(today, time)
    return today + datetime.timedelta(days=today.weekday() - weekday)


class Request(models.Model):
    """Stores the data of a lesson request"""

    time_availability = models.TimeField(blank=False)

    day_availability = models.IntegerField(choices=settings.DAYS_OF_THE_WEEK, blank=False)

    lesson_interval = models.IntegerField(choices=settings.LESSON_INTERVALS, blank=False)

    lesson_count = models.IntegerField(
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    lesson_duration = models.IntegerField(choices=settings.LESSON_DURATIONS, blank=False)

    preferred_teacher = models.CharField(blank=True, max_length=50)

    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=False)

    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)

    is_approved = models.BooleanField(default=False)

    @property
    def availability(self):
        """Gets the availability in full"""
        day_of_the_week = settings.DAYS_OF_THE_WEEK[int(self.day_availability)][1]
        return "%s %s" % (day_of_the_week, self.time_availability)

    def generate_lessons(self, teacher):
        """Generates lessons on the provided day/time at weekly intervals"""
        self.is_approved = True

        lesson_datetime = get_date_from_weekday(
            self.day_availability,
            self.time_availability
        )

        # Generate Lessons for the request
        for i in range(self.lesson_count):
            lesson = Lesson(
                teacher=teacher,
                student=self.student,
                date=lesson_datetime,
                instrument=self.instrument,
                duration=self.lesson_duration
            )
            lesson.save()

            lesson_datetime += datetime.timedelta(weeks=self.lesson_interval)

        self.save()

        # Generate Invoices for the lessons
        price = self.instrument.base_price * self.lesson_duration / 60
        invoice = Invoice(price=price, lesson=lesson)
        invoice.save()


class Invoice(models.Model):
    price = models.IntegerField(blank=False)
    paid = models.BooleanField(default=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=False)


class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    note = models.CharField(blank=True, max_length=25)
    change = models.CharField(blank=False, max_length=25)
    old_balance = models.IntegerField(blank=False)
    new_balance = models.IntegerField(blank=False)
