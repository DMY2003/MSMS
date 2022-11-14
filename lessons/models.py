from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)

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

class Request(models.Model):
    student_availability = models.DateTimeField(blank=False)
    lesson_count = models.IntegerField(blank=False)
    lesson_duration = models.IntegerField(blank=False)
    preferred_teacher = models.TextField()
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    is_approved = models.BooleanField(default=False)