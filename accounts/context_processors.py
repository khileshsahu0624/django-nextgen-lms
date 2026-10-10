from .models import ModuleCategory

def sidebar_menu(request):
    """
    Context processor to fetch all module categories and their modules
    ordered by their respective 'order' fields.
    """
    from django.db.models import Prefetch
    from .models import Module
    
    # We only want to prefetch modules that might be used in the sidebar
    categories = ModuleCategory.objects.prefetch_related(
        Prefetch('modules', queryset=Module.objects.order_by('order'))
    ).order_by('order')
    
    from django.urls import reverse, NoReverseMatch
    for category in categories:
        for module in category.modules.all():
            if module.url_name:
                try:
                    module.resolved_url = reverse(module.url_name)
                except NoReverseMatch:
                    module.resolved_url = '#'
            else:
                module.resolved_url = '#'
    
    return {'sidebar_categories': categories}
