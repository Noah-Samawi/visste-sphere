"""Product Models"""

from decimal import Decimal
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    """
    Model representing a category.

    Defines a category with a name and an optional friendly name.
    """
    class Meta:
        """
        Meta class for the Category model.
        """
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        """
        Returns the friendly name of the product if available.
        """
        return self.friendly_name


class Product(models.Model):
    """
    Model representing a product.

    Defines a product with various attributes such as category,
    SKU, name, description, price, rating, etc.

    """
    category = models.ForeignKey('Category', null=True,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True)
    name = models.CharField(max_length=254, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                validators=[MinValueValidator(1)])
    rating = models.DecimalField(max_digits=6, decimal_places=2, default=1,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(5)])
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    sale = models.IntegerField(default=0, null=True,
                               blank=True, validators=[MinValueValidator(0),
                                                       MaxValueValidator(100)])
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate a random SKU on save if one is not provided
            self.sku = 'pp' + get_random_string(length=8)

        super().save(*args, **kwargs)

    @property
    def rating_array(self):
        # Return an array of items to be used in the template for looping
        return ['item' for _ in range(round(self.rating))]

    @property
    def total_final_price(self):
        """
        Calculate the total final price of the product, considering discounts
        and sale prices.
        """
        discounted_amount = (self.sale / Decimal(100)) * self.price
        result = self.price - discounted_amount - self.discount
        return result.quantize(Decimal('0.00'))

    def __str__(self):
        return str(self.name)
