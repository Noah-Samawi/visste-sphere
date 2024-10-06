"""This module contains custom template filters for calculating subtotal in a Django template."""

from django import template

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculates the subtotal of a product based on its price and quantity.
    """
    return price * quantity
