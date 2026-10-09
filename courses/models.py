from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser

class CourseCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CourseTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all_levels', 'All Levels'),
    )
    
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('hidden', 'Hidden'),
    )

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )

    # Identifiers & Relations
    course_category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    course_instructor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='instructed_courses')
    course_tags = models.ManyToManyField(CourseTag, blank=True, related_name='courses')
    course_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # Basic Info
    course_title = models.CharField(max_length=255, null=True, blank=True)
    course_slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    course_short_description = models.TextField(null=True, blank=True)
    course_description = models.TextField(null=True, blank=True)
    
    # Media
    course_thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    course_intro_video = models.FileField(upload_to='course_videos/', null=True, blank=True)
    
    # Details
    course_level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='beginner', null=True, blank=True)
    course_language = models.CharField(max_length=100, default='English', null=True, blank=True)
    course_duration_minutes = models.PositiveIntegerField(null=True, blank=True, help_text="Total duration in minutes")
    
    # Pricing
    course_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    course_discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    course_is_free = models.BooleanField(default=False)
    course_currency = models.CharField(max_length=10, default='INR', null=True, blank=True)
    
    # Status & Visibility
    course_visibility = models.CharField(max_length=50, choices=VISIBILITY_CHOICES, default='public', null=True, blank=True)
    course_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft', null=True, blank=True)
    
    # Timings
    course_enrollment_start_date = models.DateTimeField(null=True, blank=True)
    course_enrollment_end_date = models.DateTimeField(null=True, blank=True)
    course_access_duration_days = models.PositiveIntegerField(null=True, blank=True, help_text="Days of access after enrollment")
    
    # Content Metadata
    course_learning_outcomes = models.TextField(null=True, blank=True, help_text="What will students learn?")
    course_requirements = models.TextField(null=True, blank=True, help_text="Prerequisites")
    course_target_audience = models.TextField(null=True, blank=True, help_text="Who is this course for?")
    
    # SEO
    course_meta_title = models.CharField(max_length=255, null=True, blank=True)
    course_meta_description = models.TextField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.course_title and not self.course_slug:
            self.course_slug = slugify(self.course_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_title or "Untitled Course"
