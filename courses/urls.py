from django.urls import path
from .views import (
    CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    TagListView, TagCreateView, TagUpdateView, TagDeleteView
)

urlpatterns = [
    # Courses
    path('', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('update/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),
    
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/create/', TagCreateView.as_view(), name='tag_create'),
    path('tags/update/<int:pk>/', TagUpdateView.as_view(), name='tag_update'),
    path('tags/delete/<int:pk>/', TagDeleteView.as_view(), name='tag_delete'),
]
