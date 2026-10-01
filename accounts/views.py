from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group, Permission
from .models import CustomUser

from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
import random

# ==========================================
# USER CRUD VIEWS
# ==========================================
class UserListView(ListView):
    model = CustomUser
    template_name = 'admin/users/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'admin/users/user_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'password', 'groups']
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        form.save_m2m()
        return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'admin/users/user_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_active', 'groups']
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'admin/users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


# ==========================================
# ROLE (GROUP) & PERMISSION CRUD VIEWS
# ==========================================
class RoleListView(ListView):
    model = Group
    template_name = 'admin/roles/role_list.html'
    context_object_name = 'roles'

class RoleCreateView(CreateView):
    model = Group
    template_name = 'admin/roles/role_form.html'
    fields = ['name', 'permissions']
    success_url = reverse_lazy('role_list')

class RoleUpdateView(UpdateView):
    model = Group
    template_name = 'admin/roles/role_form.html'
    fields = ['name', 'permissions']
    success_url = reverse_lazy('role_list')

class RoleDeleteView(DeleteView):
    model = Group
    template_name = 'admin/roles/role_confirm_delete.html'
    success_url = reverse_lazy('role_list')


# ==========================================
# API ENDPOINTS FOR FRONTEND MODALS
# ==========================================
@csrf_exempt
def api_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already exists.'})
            if CustomUser.objects.filter(phone_number=phone).exists():
                return JsonResponse({'status': 'error', 'message': 'Phone number already exists.'})

            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                phone_number=phone,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='student'
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
            
            user = CustomUser.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            
            # Print OTP in terminal for testing
            print(f"\n======================================")
            print(f" OTP for {user.email} is: {otp} ")
            print(f"======================================\n")
            
            return JsonResponse({'status': 'success', 'message': 'OTP sent successfully to your registered device.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found. Please register first.'})
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