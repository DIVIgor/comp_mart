from django.urls import path

from . import views


app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:cat_slug>/', views.products, name='products'),
    path('<slug:cat_slug>/<slug:prod_slug>', views.product, name='product')
]