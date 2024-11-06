from .models import NavigationItem

def navigation(request):
    nav_items = NavigationItem.objects.filter(is_active=True, parent=None).order_by('order')
    return {'nav_items': nav_items}