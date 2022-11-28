from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


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
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=50, blank=False, unique=False)
    last_name = models.CharField(max_length=50, blank=False, unique=False)

    @property
    def full_name(self):
        """Gets the full name of a teacher"""
        return "%s %s" % (self.first_name, self.last_name)

class Administrator(User):
    pass

class Director(User):
    pass


class Lesson(models.Model):
    time = models.DateTimeField(blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)


class Instrument(models.Model):
    name = models.CharField(max_length=30, blank=False)

class Request(models.Model):
    time_availability = models.TimeField(null=True)
    day_availability = models.CharField(max_length=10, blank=True)
    lesson_interval = models.IntegerField(default=1)
    lesson_count = models.IntegerField(blank=False)
    lesson_duration = models.IntegerField(blank=False)
    preferred_teacher = models.TextField()
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    is_approved = models.BooleanField(default=False)

    @property
    def availability(self):
        """Gets the availability in full form"""
        return "%s %s" % (self.day_availability, self.time_availability)

class Invoice(models.Model):
    price = models.IntegerField(blank=False)
    paid = models.BooleanField(default=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=False)



