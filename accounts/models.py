from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # We will use email for authentication instead of username
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # --- LMS Specific Profile Fields ---
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    
    # --- Address Fields ---
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    
    # --- Student Specific Fields ---
    student_code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_phone = models.CharField(max_length=15, null=True, blank=True)
    
    # --- Professional / Instructor Fields ---
    bio = models.TextField(null=True, blank=True, help_text="Short biography about the user")
    qualification = models.CharField(max_length=255, null=True, blank=True, help_text="Highest qualification or degree")
    
    # --- Social Links ---
    linkedin_link = models.URLField(max_length=255, null=True, blank=True)
    facebook_link = models.URLField(max_length=255, null=True, blank=True)
    twitter_link = models.URLField(max_length=255, null=True, blank=True)

    # Optional explicitly defined role if you don't want to strictly use Django Groups
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    # --- Enrollment & Payment Fields ---
    course = models.CharField(max_length=100, null=True, blank=True)
    batch = models.CharField(max_length=100, null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    
    ENROLLMENT_STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('pending', 'Pending'),
        ('dropped', 'Dropped'),
        ('graduated', 'Graduated'),
    )
    enrollment_status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='pending', null=True, blank=True)
    
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
    )
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid', null=True, blank=True)

    # Fields for OTP Verification
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role.name if self.role else 'No Role'})"

class Role(models.Model):
    """
    Represents the roles in the 'User Roles' dropdown (e.g., Super Admin, HR, Manager)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ModuleCategory(models.Model):
    """
    Represents the collapsible headers in your UI 
    (e.g., 'Settings Configuration', 'Attendance Settings Configuration')
    """
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which it appears in the UI")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Module(models.Model):
    """
    Represents the individual rows in your UI 
    (e.g., 'Payslip Configuration', 'Business Settings')
    """
    category = models.ForeignKey(ModuleCategory, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} -> {self.name}"

class RolePermission(models.Model):
    """
    Represents the actual checkboxes (Create, Read, Update, Delete).
    The 'All' checkbox is a frontend feature that toggles these 4 booleans.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='role_permissions')
    
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'module')

    def __str__(self):
        return f"{self.role.name} - {self.module.name} Permissions"

    @property
    def can_do_all(self):
        """Helper to check if all permissions are granted (for the 'All' checkbox status)"""
        return all([self.can_create, self.can_read, self.can_update, self.can_delete])


class FhMenu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    menu_p = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_menus', db_column='menu_p_id')
    menu_route_type_id = models.IntegerField(null=True, blank=True)
    menu_name = models.CharField(max_length=127, null=True, blank=True)
    menu_icon = models.CharField(max_length=50, null=True, blank=True)
    menu_status = models.BooleanField(default=True, null=True, blank=True)
    menu_sub_status = models.IntegerField(default=0)
    menu_route = models.CharField(max_length=255, null=True, blank=True)
    menu_group = models.CharField(max_length=55, null=True, blank=True)
    menu_mdl_id = models.IntegerField(null=True, blank=True)
    menu_sequence = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fh_menus'
        ordering = ['menu_sequence']

    def __str__(self):
        return self.menu_name or f"Menu {self.menu_id}"

