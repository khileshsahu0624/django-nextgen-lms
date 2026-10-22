from .models import ModuleCategory, RolePermission, CustomUser
from courses.models import Course

def sidebar_menu(request):
    """
    Context processor to fetch all module categories and their modules
    ordered by their respective 'order' fields, with user role permission checks
    and dynamic notification badges.
    """
    from django.db.models import Prefetch
    from .models import Module
    from django.urls import reverse, NoReverseMatch

    user = getattr(request, 'user', None)
    is_authenticated = user and user.is_authenticated
    user_role = getattr(user, 'role', None) if is_authenticated else None
    role_name = user_role.name.lower() if user_role else ''
    is_admin = is_authenticated and (user.is_superuser or user.is_staff or 'admin' in role_name or 'manager' in role_name or 'head' in role_name)

    # Permission lookup cache for the user's role
    allowed_module_ids = None
    if is_authenticated and not is_admin and user_role:
        allowed_module_ids = set(
            RolePermission.objects.filter(
                role=user_role,
                can_read=True
            ).values_list('module_id', flat=True)
        )

    categories = ModuleCategory.objects.prefetch_related(
        Prefetch('modules', queryset=Module.objects.order_by('order'))
    ).order_by('order')

    filtered_categories = []
    
    # Calculate dynamic badge counts safely
    try:
        users_count = CustomUser.objects.count()
        courses_count = Course.objects.count()
    except Exception:
        users_count = 0
        courses_count = 0

    for category in categories:
        permitted_modules = []
        for module in category.modules.all():
            # If not admin, check if module read permission is granted
            if allowed_module_ids is not None and module.id not in allowed_module_ids:
                continue

            current_url_name = getattr(request.resolver_match, 'url_name', '') or ''
            if module.url_name:
                try:
                    module.resolved_url = reverse(module.url_name)
                    # Check exact match first
                    if current_url_name == module.url_name:
                        module.is_active = True
                    # Only match child CRUD actions if this module is a _list view (e.g. user_list -> user_create, user_update)
                    elif module.url_name.endswith('_list'):
                        crud_base = module.url_name[:-5]  # remove '_list'
                        module.is_active = current_url_name in [f"{crud_base}_create", f"{crud_base}_update", f"{crud_base}_delete", f"{crud_base}_detail"]
                    else:
                        module.is_active = False
                except NoReverseMatch:
                    module.resolved_url = '#'
                    module.is_active = False
            else:
                module.resolved_url = '#'
                module.is_active = False

            # Attach dynamic badges
            m_name = module.name.lower()
            if 'students' in m_name:
                module.badge_count = users_count
                module.badge_color = '#e0f2fe'
                module.badge_text_color = '#0369a1'
            elif 'course' in m_name:
                module.badge_count = courses_count
                module.badge_color = '#ecfdf5'
                module.badge_text_color = '#047857'
            else:
                module.badge_count = None

            permitted_modules.append(module)

        if permitted_modules:
            category.permitted_modules = permitted_modules
            filtered_categories.append(category)

    return {'sidebar_categories': filtered_categories}
