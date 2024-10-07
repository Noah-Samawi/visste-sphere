"""Product forms"""
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    A form for creating or editing products.

    """
    class Meta:
        """Get product model, choose fields to display"""

        model = Product
        fields = ['name', 'description', 'price', 'image',
                  'category', 'sale', 'rating']
