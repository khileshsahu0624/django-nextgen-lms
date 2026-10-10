from django.urls import path
from . import views


urlpatterns = [
    path('', views.student_list, name='old_student_list'),
    path('student/<int:id>/', views.student_detail, name='old_student_detail'),
    path('student/add/', views.student_create, name='old_student_create'),
    path('student/<int:id>/edit/', views.student_update, name='old_student_update'),
    path('student/<int:id>/delete/', views.student_delete, name='old_student_delete'),
]