"""Checkout Admin Models"""

from django.contrib import admin
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .models import Order, OrderLineItem


class OrderLineItemAdminForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = '__all__'
     

    def __init__(self, *args, **kwargs):

        """
        Initialize the form and set the content type queryset to only include
        products, programs and subscriptions.
        """
        super().__init__(*args, **kwargs)
        self.fields['content_type'].queryset = \
            ContentType.objects.filter(
                model__in=['program', 'product', 'subscription']
                )

    def clean_object_id(self):
        """
        Clean method for the object_id field. Ensures
        content id is valid for the selected content type.

        """
        content_type = self.cleaned_data.get('content_type')
        object_id = self.cleaned_data.get('object_id')

        if content_type:
            model_class = content_type.model_class()
            if not model_class.objects.filter(id=object_id).exists():
                raise ValidationError(
                    'Invalid object ID for the selected content type.'
                    )
        return object_id

    def clean_quantity(self):
        """
        Clean method for the quantity field.
        Ensures quantity is greater than zero.

        """
        quantity = self.cleaned_data.get('quantity')

        if quantity == 0:
            raise ValidationError(
                'Quantity must be greater than zero.'
                )
        return quantity


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline admin class for displaying order line items in the admin panel.

    """
    form = OrderLineItemAdminForm
    model = OrderLineItem
    readonly_fields = ('lineitem_total', 'item_total')

    extra = 0

    def get_content_object_name(self, obj):
        """
        Method to get the name of the associated content object.

        """
        return obj.content_object.name


class OrderAdmin(admin.ModelAdmin):
    """
    Admin class for managing orders in the admin panel.
    """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_cart',
                       'stripe_pid')

    fields = ('order_number', "user_profile", 'date', 'full_name',
              'email', 'phone_number',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_cart',
              'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
