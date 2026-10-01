from django.urls import path
from . import views

urlpatterns = [
    # User CRUD
    path('admin/users/', views.UserListView.as_view(), name='user_list'),
    path('admin/users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('admin/users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('admin/users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # Role CRUD (Groups)
    path('admin/roles/', views.RoleListView.as_view(), name='role_list'),
    path('admin/roles/create/', views.RoleCreateView.as_view(), name='role_create'),
    path('admin/roles/<int:pk>/update/', views.RoleUpdateView.as_view(), name='role_update'),
    path('admin/roles/<int:pk>/delete/', views.RoleDeleteView.as_view(), name='role_delete'),

    # Simple API Endpoints for Frontend Modals
    path('api/signup/', views.api_signup, name='api_signup'),
    path('api/send-otp/', views.api_send_otp, name='api_send_otp'),
    path('api/verify-login/', views.api_verify_login, name='api_verify_login'),
]
