from django.db import models
from account.models import CMUserBase
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:products', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='product', on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        CMUserBase, related_name='product_creator', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/no_image_available.png')
    slug = models.SlugField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'products'
        ordering = ('-created',)

    def __str__(self):
        """String view of description"""
        if len(self.description) > 215:
            return f"{self.description[:215]}..."
        else:
            return f"{self.description}"

    # function for use dynamic urls by slug in product store urls
    def get_absolute_url(self):
        return reverse('store:product', args=[self.category.slug, self.slug])