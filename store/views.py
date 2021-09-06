from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .models import Category, Product


def home(request):
    """Homepage comp_mart app"""
    return render(request, 'store/home.html')

def products(request, cat_slug):
    """List of products page by requested category"""
    products = Product.objects.filter(category__slug=cat_slug)
    context = {'products': products, 'category': cat_slug}
    return render(request, 'store/products/products.html', context)

def categories(request):
    """List of categories"""
    return {'categories': Category.objects.all()}

def product(request, cat_slug, prod_slug):
    """Product page"""
    product = get_object_or_404(Product, slug=prod_slug, in_stock=True)
    context = {'category': cat_slug,'product': product}
    return render(request, 'store/products/product.html', context)