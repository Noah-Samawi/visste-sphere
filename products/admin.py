"Product Admin Models"

from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.

    Defines the display fields for the Category admin panel.
    """
    list_display = (
        'friendly_name',
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.

    Defines the display fields and ordering for the Product admin panel.
    """

    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
