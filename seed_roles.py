import os
import django
from accounts.models import Role

roles = ["Admin", "Instructor", "Student"]

for role_name in roles:
    Role.objects.get_or_create(name=role_name, defaults={'description': f'Default {role_name} Role'})
    print(f"Role {role_name} checked/created.")
