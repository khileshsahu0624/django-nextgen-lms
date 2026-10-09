from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Course, CourseCategory, CourseTag

# --- CATEGORY VIEWS ---
class CategoryListView(ListView):
    model = CourseCategory
    template_name = 'admin/courses/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = CourseCategory
    template_name = 'admin/courses/category_form.html'
    fields = ['name', 'slug']
    success_url = reverse_lazy('category_list')
    success_message = "Category created successfully!"

class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = CourseCategory
    template_name = 'admin/courses/category_form.html'
    fields = ['name', 'slug']
    success_url = reverse_lazy('category_list')
    success_message = "Category updated successfully!"

class CategoryDeleteView(DeleteView):
    model = CourseCategory
    template_name = 'admin/courses/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Category deleted successfully!")
        return super().form_valid(form)

# --- TAG VIEWS ---
class TagListView(ListView):
    model = CourseTag
    template_name = 'admin/courses/tag_list.html'
    context_object_name = 'tags'

class TagCreateView(SuccessMessageMixin, CreateView):
    model = CourseTag
    template_name = 'admin/courses/tag_form.html'
    fields = ['name', 'slug']
    success_url = reverse_lazy('tag_list')
    success_message = "Tag created successfully!"

class TagUpdateView(SuccessMessageMixin, UpdateView):
    model = CourseTag
    template_name = 'admin/courses/tag_form.html'
    fields = ['name', 'slug']
    success_url = reverse_lazy('tag_list')
    success_message = "Tag updated successfully!"

class TagDeleteView(DeleteView):
    model = CourseTag
    template_name = 'admin/courses/tag_confirm_delete.html'
    success_url = reverse_lazy('tag_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Tag deleted successfully!")
        return super().form_valid(form)

# --- COURSE VIEWS ---
class CourseListView(ListView):
    model = Course
    template_name = 'admin/courses/course_list.html'
    context_object_name = 'courses'

class CourseCreateView(SuccessMessageMixin, CreateView):
    model = Course
    template_name = 'admin/courses/course_form.html'
    fields = [
        'course_category', 'course_tags', 'course_instructor', 'course_code', 'course_title',
        'course_slug', 'course_short_description', 'course_description',
        'course_thumbnail', 'course_intro_video', 'course_level',
        'course_language', 'course_duration_minutes', 'course_price',
        'course_discount_price', 'course_is_free', 'course_currency',
        'course_visibility', 'course_status', 'course_enrollment_start_date',
        'course_enrollment_end_date', 'course_access_duration_days',
        'course_learning_outcomes', 'course_requirements', 'course_target_audience',
        'course_meta_title', 'course_meta_description'
    ]
    success_url = reverse_lazy('course_list')
    success_message = "Course created successfully!"

class CourseUpdateView(SuccessMessageMixin, UpdateView):
    model = Course
    template_name = 'admin/courses/course_form.html'
    fields = [
        'course_category', 'course_tags', 'course_instructor', 'course_code', 'course_title',
        'course_slug', 'course_short_description', 'course_description',
        'course_thumbnail', 'course_intro_video', 'course_level',
        'course_language', 'course_duration_minutes', 'course_price',
        'course_discount_price', 'course_is_free', 'course_currency',
        'course_visibility', 'course_status', 'course_enrollment_start_date',
        'course_enrollment_end_date', 'course_access_duration_days',
        'course_learning_outcomes', 'course_requirements', 'course_target_audience',
        'course_meta_title', 'course_meta_description'
    ]
    success_url = reverse_lazy('course_list')
    success_message = "Course updated successfully!"

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'admin/courses/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Course deleted successfully!")
        return super().form_valid(form)
