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
@login_required(login_url='/')
def dashboard_view(request):
    return render(request, 'admin/dashboard.html')
