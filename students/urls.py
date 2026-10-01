from django.urls import path
from . import views


urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    path('student/add/', views.student_create, name='student_create'),
    path('student/<int:id>/edit/', views.student_update, name='student_update'),
    path('student/<int:id>/delete/', views.student_delete, name='student_delete'),
]