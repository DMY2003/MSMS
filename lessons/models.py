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