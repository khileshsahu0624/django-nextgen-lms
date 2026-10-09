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

    # Module CRUD
    path('admin/modules/', views.ModuleListView.as_view(), name='module_list'),
    path('admin/modules/create/', views.ModuleCreateView.as_view(), name='module_create'),
    path('admin/modules/<int:pk>/update/', views.ModuleUpdateView.as_view(), name='module_update'),
    path('admin/modules/<int:pk>/delete/', views.ModuleDeleteView.as_view(), name='module_delete'),

    # Simple API Endpoints for Frontend Modals
    path('api/signup/', views.api_signup, name='api_signup'),
    path('api/send-otp/', views.api_send_otp, name='api_send_otp'),
    path('api/verify-login/', views.api_verify_login, name='api_verify_login'),
    
    # API Endpoints for Role & Permission CRUD
    path('api/roles/', views.api_get_roles, name='api_get_roles'),
    path('api/roles/create/', views.api_create_role, name='api_create_role'),
    path('api/roles/<int:role_id>/update/', views.api_update_role, name='api_update_role'),
    path('api/roles/<int:role_id>/delete/', views.api_delete_role, name='api_delete_role'),
    path('api/roles/<int:role_id>/permissions/', views.api_get_role_permissions, name='api_get_role_permissions'),
    path('api/roles/<int:role_id>/permissions/update/', views.api_update_role_permissions, name='api_update_role_permissions'),
]
