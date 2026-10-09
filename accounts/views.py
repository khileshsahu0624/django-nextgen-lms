from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, Role

from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.db.models import Prefetch
from .models import CustomUser, Role, ModuleCategory, Module, RolePermission
# USER CRUD VIEWS
# ==========================================
class UserListView(ListView):
    model = CustomUser
    template_name = 'admin/users/user_list.html'
    context_object_name = 'users'
    queryset = CustomUser.objects.order_by('-id')

class UserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'admin/users/user_form.html'
    fields = [
        'first_name', 'last_name', 'email', 'phone_number', 'role', 'password',
        'profile_photo', 'gender', 'dob', 'address', 'city', 'state', 'country', 'pincode',
        'guardian_name', 'guardian_phone',
        'course', 'batch', 'admission_date', 'enrollment_status',
        'payment_amount', 'payment_date', 'payment_status',
        'bio', 'qualification', 'linkedin_link', 'facebook_link', 'twitter_link'
    ]
    success_url = reverse_lazy('user_list')
    success_message = "User created successfully!"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        # Auto-generate student_code after saving to use the auto-incremented ID
        user.student_code = f"STU{user.id:05d}"
        user.save()
        
        # Set self.object and return HttpResponseRedirect directly to avoid double save issues
        self.object = user
        messages.success(self.request, self.success_message)
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())

class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'admin/users/user_form.html'
    fields = [
        'first_name', 'last_name', 'email', 'phone_number', 'role', 'is_active',
        'profile_photo', 'gender', 'dob', 'address', 'city', 'state', 'country', 'pincode',
        'guardian_name', 'guardian_phone',
        'course', 'batch', 'admission_date', 'enrollment_status',
        'payment_amount', 'payment_date', 'payment_status',
        'bio', 'qualification', 'linkedin_link', 'facebook_link', 'twitter_link'
    ]
    success_url = reverse_lazy('user_list')
    success_message = "User updated successfully!"

    def form_valid(self, form):
        user = form.save(commit=False)
        if not user.student_code:
            user.student_code = f"STU{user.id:05d}"
        user.save()
        
        self.object = user
        messages.success(self.request, self.success_message)
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())

class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'admin/users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, "User deleted successfully!")
        return super().form_valid(form)


# ==========================================
# ROLE CRUD VIEWS
# ==========================================
class RoleListView(ListView):
    model = Role
    template_name = 'admin/roles/role_list.html'
    context_object_name = 'roles'
    queryset = Role.objects.order_by('-id')

class RoleCreateView(SuccessMessageMixin, CreateView):
    model = Role
    template_name = 'admin/roles/role_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('role_list')
    success_message = "Role created successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ModuleCategory.objects.prefetch_related('modules').order_by('order')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Process permissions from POST data
        modules = Module.objects.all()
        for module in modules:
            can_create = self.request.POST.get(f'create_{module.id}') == 'on'
            can_read = self.request.POST.get(f'read_{module.id}') == 'on'
            can_update = self.request.POST.get(f'update_{module.id}') == 'on'
            can_delete = self.request.POST.get(f'delete_{module.id}') == 'on'
            
            if can_create or can_read or can_update or can_delete:
                RolePermission.objects.update_or_create(
                    role=self.object, 
                    module=module,
                    defaults={
                        'can_create': can_create,
                        'can_read': can_read,
                        'can_update': can_update,
                        'can_delete': can_delete
                    }
                )
            else:
                RolePermission.objects.filter(role=self.object, module=module).delete()
        return response

class RoleUpdateView(SuccessMessageMixin, UpdateView):
    model = Role
    template_name = 'admin/roles/role_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('role_list')
    success_message = "Role updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pre-fetch the role permissions and attach them to modules dynamically for the template
        categories = ModuleCategory.objects.prefetch_related('modules').order_by('order')
        
        for category in categories:
            for module in category.modules.all():
                try:
                    module.perm = RolePermission.objects.get(role=self.object, module=module)
                except RolePermission.DoesNotExist:
                    module.perm = None
                    
        context['categories'] = categories
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Process permissions from POST data
        modules = Module.objects.all()
        for module in modules:
            can_create = self.request.POST.get(f'create_{module.id}') == 'on'
            can_read = self.request.POST.get(f'read_{module.id}') == 'on'
            can_update = self.request.POST.get(f'update_{module.id}') == 'on'
            can_delete = self.request.POST.get(f'delete_{module.id}') == 'on'
            
            if can_create or can_read or can_update or can_delete:
                RolePermission.objects.update_or_create(
                    role=self.object, 
                    module=module,
                    defaults={
                        'can_create': can_create,
                        'can_read': can_read,
                        'can_update': can_update,
                        'can_delete': can_delete
                    }
                )
            else:
                RolePermission.objects.filter(role=self.object, module=module).delete()
        return response

class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'admin/roles/role_confirm_delete.html'
    success_url = reverse_lazy('role_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Role deleted successfully!")
        return super().form_valid(form)


# ==========================================
# MODULE CRUD VIEWS
# ==========================================
class ModuleListView(ListView):
    model = Module
    template_name = 'admin/modules/module_list.html'
    context_object_name = 'modules'
    queryset = Module.objects.select_related('category').order_by('-id')

class ModuleCreateView(SuccessMessageMixin, CreateView):
    model = Module
    template_name = 'admin/modules/module_form.html'
    fields = ['category', 'name']
    success_url = reverse_lazy('module_list')
    success_message = "Module created successfully!"

class ModuleUpdateView(SuccessMessageMixin, UpdateView):
    model = Module
    template_name = 'admin/modules/module_form.html'
    fields = ['category', 'name']
    success_url = reverse_lazy('module_list')
    success_message = "Module updated successfully!"

class ModuleDeleteView(DeleteView):
    model = Module
    template_name = 'admin/modules/module_confirm_delete.html'
    success_url = reverse_lazy('module_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Module deleted successfully!")
        return super().form_valid(form)


# ==========================================
# API ENDPOINTS FOR FRONTEND MODALS
# ==========================================
@csrf_exempt
def api_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            password = data.get('password', '')
            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()

            import re
            
            if not email or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'status': 'error', 'message': 'Invalid email format.'})
            
            if not phone or not re.match(r'^\d{10}$', phone):
                return JsonResponse({'status': 'error', 'message': 'Phone number must be 10 digits.'})
                
            if not password or not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$', password):
                return JsonResponse({'status': 'error', 'message': 'Password must be at least 8 characters long, with 1 uppercase, 1 lowercase, 1 number, and 1 special character.'})

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already exists.'})
            if CustomUser.objects.filter(phone_number=phone).exists():
                return JsonResponse({'status': 'error', 'message': 'Phone number already exists.'})

            student_role, _ = Role.objects.get_or_create(name='student')
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                phone_number=phone,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=student_role
            )
            return JsonResponse({'status': 'success', 'message': 'Registration successful!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def api_send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'User not found. Please register first.'})
            
            user = authenticate(username=email, password=password)
            if user is None:
                return JsonResponse({'status': 'error', 'message': 'Incorrect password.'})
                
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            
            # Print OTP in terminal for testing
            print(f"\n======================================")
            print(f" OTP for {user.email} is: {otp} ")
            print(f"======================================\n")
            
            return JsonResponse({'status': 'success', 'message': 'OTP sent successfully to your registered device.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def api_verify_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            otp = data.get('otp')
            
            user = CustomUser.objects.get(email=email)
            if user.otp == otp:
                user.is_phone_verified = True
                user.otp = None 
                user.save()
                
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Logged in successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


# ==========================================
# API CRUD FOR ROLES AND PERMISSIONS
# ==========================================

@csrf_exempt
def api_get_roles(request):
    """Fetch all roles"""
    if request.method == 'GET':
        roles = Role.objects.all().values('id', 'name', 'description')
        return JsonResponse({'status': 'success', 'data': list(roles)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def api_create_role(request):
    """Create a new role"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description', '')
            
            if Role.objects.filter(name__iexact=name).exists():
                return JsonResponse({'status': 'error', 'message': 'Role with this name already exists'})
                
            role = Role.objects.create(name=name, description=description)
            return JsonResponse({'status': 'success', 'message': 'Role created successfully', 'data': {'id': role.id, 'name': role.name}})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def api_update_role(request, role_id):
    """Update a role's basic info"""
    if request.method == 'PUT' or request.method == 'POST':
        try:
            data = json.loads(request.body)
            role = Role.objects.get(id=role_id)
            
            name = data.get('name')
            if name:
                if Role.objects.filter(name__iexact=name).exclude(id=role_id).exists():
                    return JsonResponse({'status': 'error', 'message': 'Another role with this name already exists'})
                role.name = name
                
            if 'description' in data:
                role.description = data.get('description')
                
            role.save()
            return JsonResponse({'status': 'success', 'message': 'Role updated successfully'})
        except Role.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Role not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def api_delete_role(request, role_id):
    """Delete a role"""
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            role = Role.objects.get(id=role_id)
            role.delete()
            return JsonResponse({'status': 'success', 'message': 'Role deleted successfully'})
        except Role.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Role not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def api_get_role_permissions(request, role_id):
    """Fetch all permissions for a specific role, grouped by Category"""
    if request.method == 'GET':
        try:
            role = Role.objects.get(id=role_id)
            
            categories = ModuleCategory.objects.prefetch_related(
                Prefetch(
                    'modules',
                    queryset=Module.objects.prefetch_related(
                        Prefetch(
                            'role_permissions',
                            queryset=RolePermission.objects.filter(role=role),
                            to_attr='current_permission'
                        )
                    )
                )
            ).order_by('order')

            result = []
            for category in categories:
                cat_data = {
                    'category_id': category.id,
                    'category_name': category.name,
                    'modules': []
                }
                for module in category.modules.all():
                    perm = module.current_permission[0] if module.current_permission else None
                    
                    mod_data = {
                        'module_id': module.id,
                        'module_name': module.name,
                        'permissions': {
                            'permission_id': perm.id if perm else None,
                            'can_create': perm.can_create if perm else False,
                            'can_read': perm.can_read if perm else False,
                            'can_update': perm.can_update if perm else False,
                            'can_delete': perm.can_delete if perm else False,
                            'can_do_all': perm.can_do_all if perm else False,
                        }
                    }
                    cat_data['modules'].append(mod_data)
                result.append(cat_data)
                
            return JsonResponse({'status': 'success', 'role': role.name, 'data': result})
        except Role.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Role not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def api_update_role_permissions(request, role_id):
    """
    Update multiple permissions for a role at once.
    """
    if request.method == 'PUT' or request.method == 'POST':
        try:
            role = Role.objects.get(id=role_id)
            data = json.loads(request.body)
            permissions_data = data.get('permissions', [])
            
            for perm in permissions_data:
                module_id = perm.get('module_id')
                RolePermission.objects.filter(role=role, module_id=module_id).update(
                    can_create=perm.get('can_create', False),
                    can_read=perm.get('can_read', False),
                    can_update=perm.get('can_update', False),
                    can_delete=perm.get('can_delete', False)
                )
                
            return JsonResponse({'status': 'success', 'message': 'Permissions updated successfully'})
        except Role.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Role not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})