from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def home(request):
    """Homepage comp_mart app"""
    return render(request, 'store/home.html')

def products(request, cat_slug):
    """List of products page by requested category"""
    category = get_object_or_404(Category, slug=cat_slug)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'store/products/products.html', context)

def product(request, cat_slug, prod_slug):
    """Product page"""
    product = get_object_or_404(Product, slug=prod_slug, in_stock=True)
    context = {'category': cat_slug,'product': product}
    return render(request, 'store/products/product.html', context)