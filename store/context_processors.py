from .models import Category

def categories(request):
    """List of categories"""
    return {'categories': Category.objects.all()}