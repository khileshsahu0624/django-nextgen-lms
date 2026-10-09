from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, ModuleCategory, Module, RolePermission

admin.site.register(Role)
admin.site.register(ModuleCategory)
admin.site.register(Module)
admin.site.register(RolePermission)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'role', 'is_phone_verified', 'is_staff']
    list_filter = ['role', 'is_phone_verified', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'phone_number', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile & Role', {'fields': ('phone_number', 'role', 'is_phone_verified', 'otp', 'otp_created_at')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Profile & Role', {'fields': ('email', 'phone_number', 'role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
