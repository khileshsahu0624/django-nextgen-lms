import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_project.settings') # Adjust 'core.settings' if your main app name is different
django.setup()

from accounts.models import ModuleCategory, Module

def seed():
    print("Clearing existing modules...")
    ModuleCategory.objects.all().delete()
    Module.objects.all().delete()

    # 1. Create Categories
    dashboard_cat, _ = ModuleCategory.objects.get_or_create(name='Core', order=1)
    users_cat, _ = ModuleCategory.objects.get_or_create(name='Users & Roles', order=2)
    academic_cat, _ = ModuleCategory.objects.get_or_create(name='Academic & Content', order=3)
    sales_cat, _ = ModuleCategory.objects.get_or_create(name='Sales & Finance', order=4)
    engagement_cat, _ = ModuleCategory.objects.get_or_create(name='Engagement', order=5)
    system_cat, _ = ModuleCategory.objects.get_or_create(name='System & Settings', order=6)

    # 2. Create Modules
    modules_data = [
        # Core
        (dashboard_cat, 'Dashboard Overview'),
        
        # Users & Roles
        (users_cat, 'Students'),
        (users_cat, 'Instructors'),
        (users_cat, 'Roles & Permissions'),
        
        # Academic & Content
        (academic_cat, 'All Courses'),
        (academic_cat, 'Categories & Tags'),
        (academic_cat, 'Pending Approvals'),
        (academic_cat, 'Video & Asset Library'),
        (academic_cat, 'Certificates'),
        
        # Sales & Finance
        (sales_cat, 'Transactions'),
        (sales_cat, 'Instructor Payouts'),
        (sales_cat, 'Coupons & Discounts'),
        
        # Engagement
        (engagement_cat, 'Announcements'),
        (engagement_cat, 'Q&A / Discussions'),
        (engagement_cat, 'Reviews & Ratings'),
        
        # System & Settings
        (system_cat, 'Advanced Reports'),
        (system_cat, 'Payment Gateways'),
        (system_cat, 'Platform Settings'),
    ]

    for category, module_name in modules_data:
        Module.objects.get_or_create(category=category, name=module_name)
        print(f"Added Module: {module_name} under {category.name}")

    print("Successfully seeded modules!")

if __name__ == '__main__':
    seed()
