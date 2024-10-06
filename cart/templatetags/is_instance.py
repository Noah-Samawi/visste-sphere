"""Custom template tags for checking the instance of an item."""

from django import template
from products.models import Product
from profiles.models import Subscription

register = template.Library()

@register.filter(name='is_product')
def is_product(value):
    return isinstance(value, Product)

@register.filter(name='is_subscription')
def is_product(value):
    return isinstance(value, Subscription)