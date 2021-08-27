from django.shortcuts import render

from .models import Category, Product


def home(request):
    """Homepage comp_mart app"""
    return render(request, 'store/home.html')

def products(request):
    """List of products page"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/products.html', context)

def categories(request):
    """List of categories"""
    return {'categories': Category.objects.all()}