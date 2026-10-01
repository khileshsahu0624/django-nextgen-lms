from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'phone',
        'phone2',
        'course',
        'age',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'name',
        'email',
        'phone',
        'course',
    )

    list_filter = (
        'course',
        'age',
        'created_at',
    )

    ordering = ('-created_at',)