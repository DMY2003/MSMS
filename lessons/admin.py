"""Configuration of the admin interface for microblogs."""
from django.contrib import admin
from .models import User, Request, Lesson, Instrument, Teacher

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active',
    ]

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for teachers."""
    pass

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for requests."""
    
    list_display = [
        "day_availability", "time_availability",
        "lesson_count", "lesson_duration", "preferred_teacher",
        "instrument", "student", "is_approved"
    ]

@admin.register(Instrument)
class RequestAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for requests."""
    pass

@admin.register(Lesson)
class RequestAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for lessons."""

    list_display = [
        "date", "teacher", "student"
    ]
