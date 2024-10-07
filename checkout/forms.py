"""Checkout Forms"""

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form for collecting user information for placing an order.
    """

    class Meta:
        """
        Metadata for the OrderForm.
        """

        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county', 'user_profile',)
