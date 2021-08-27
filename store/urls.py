from django.urls import path

from . import views


app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.products, name='products'),
    # path('product', views.product, name='product')
]
