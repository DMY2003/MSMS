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
    first_name = models.CharField(max_length=50, blank=False, unique=False)
    last_name = models.CharField(max_length=50, blank=False, unique=False)
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = []


class Student(User):
    balance = models.IntegerField(default=0)


class Administrator(User):
    pass


class Teacher(User):
    pass


class Lesson(models.Model):
    time = models.DateTimeField(blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)


class Instrument(models.Model):
    name = models.TextField(blank=False)


class Invoice(models.Model):
    price = models.IntegerField(blank=False)
    paid = models.BooleanField(default=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=False)


# -----------Commented temporarily to test seeder----------------

# class Request(models.Model):
#     student_availability = models.DateTimeField(blank=False)
#     lesson_count = models.IntegerField(blank=False)
#     lesson_duration = models.IntegerField(blank=False)
#     preferred_teacher = models.TextField()
#     instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=False)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
#     is_approved = models.BooleanField(default=False)

class Request(models.Model):
    student_availability = models.DateTimeField(blank=False)
    lesson_count = models.IntegerField(blank=False)
    lesson_duration = models.IntegerField(blank=False)
    preferred_teacher = models.TextField()
    instrument = models.ForeignKey(on_delete=models.CASCADE, blank=False)
    student = models.ForeignKey(on_delete=models.CASCADE, blank=False)
    is_approved = models.BooleanField(default=False)
