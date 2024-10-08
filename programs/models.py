"""Program Models"""

from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from embed_video.fields import EmbedVideoField


class Program(models.Model):
    category = models.ForeignKey('products.Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6,
                                 decimal_places=2, null=True, blank=True)
    difficulty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        null=True,
        blank=True
    )
    length = models.DurationField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    video_url = EmbedVideoField(
        default='https://www.youtube.com/watch?v=TjPFZaMe2yw'
    )
    sale = models.IntegerField(default=0, null=True, blank=True)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    @property
    def rating_array(self):
        # Return an array of items to be used in the template for looping
        return ['item' for _ in range(round(self.rating))]

    @property
    def total_final_price(self):
        discounted_amount = (self.sale / Decimal(100)) * self.price
        result = self.price - discounted_amount - self.discount
        return result.quantize(Decimal('0.00'))

    def __str__(self):
        return str(self.name)


class Module(models.Model):
    """
    Model representing a module within a program.

    """
    program = models.ForeignKey(Program,
                                on_delete=models.CASCADE,
                                related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
