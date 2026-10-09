from django.shortcuts import render

def landing_page(request):
    return render(request, 'user/index.html')

def login_view(request):
    return render(request, 'user/login.html')

def signup_view(request):
    return render(request, 'user/signup.html')

def otp_view(request):
    return render(request, 'user/otp.html')

from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required(login_url='/')
def dashboard_view(request):
    role_name = request.user.role.name.lower() if hasattr(request.user, 'role') and request.user.role else ''
    
    if request.user.is_superuser or 'admin' in role_name or 'manager' in role_name or 'head' in role_name:
        return redirect('admin_dashboard')
    elif 'instructor' in role_name or 'teacher' in role_name:
        return redirect('instructor_dashboard')
    else:
        return redirect('student_dashboard')

@login_required(login_url='/')
def admin_dashboard(request):
    return render(request, 'admin/dashboards/admin_dashboard.html')

@login_required(login_url='/')
def instructor_dashboard(request):
    return render(request, 'admin/dashboards/instructor_dashboard.html')

@login_required(login_url='/')
def student_dashboard(request):
    return render(request, 'admin/dashboards/student_dashboard.html')

@login_required(login_url='/')
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect(request.META.get('HTTP_REFERER', 'profile'))
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'user/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing_page')
