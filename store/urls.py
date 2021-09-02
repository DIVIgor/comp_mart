from django.urls import path

from . import views


app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:cat_slug>/products/', views.products, name='products'),
    path('products/<slug:prod_slug>/', views.product, name='product')
]