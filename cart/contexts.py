"Cart context functions"

from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from profiles.models import Subscription
from programs.models import Program

from .utils import get_item_from_item_id, apply_subscription_discount


def cart_contents(request):
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    total_members_discount = 0
    subscription_exists = False
    delivery_cost = settings.DELIVERY_COST

    # Set active subscription and set it as the current subscription
    if request.user.is_authenticated:
        if request.user.profile.active_subscription:
            request.user.profile.subscription = \
                request.user.profile.active_subscription
            request.user.profile.save()
            subscription_exists = True

    # Add subscription profile discount if in cart
    for item_id, item_data in cart.items():

        product = get_item_from_item_id(item_id)

        if isinstance(product, Subscription):
            if request.user.profile.active_subscription:
                if request.user.profile.active_subscription.id <= product.id:
                    request.user.profile.subscription = product
                    request.user.profile.save()
                else:
                    sub = request.user.profile.active_subscription
                    request.user.profile.subscription = sub
                    request.user.profile.save()
            else:
                request.user.profile.subscription = product
                request.user.profile.save()

            subscription_exists = True

    # Remove subscription if not in cart or profile
    if not subscription_exists and request.user.is_authenticated:
        request.user.profile.active_subscription = None
        request.user.profile.subscription = None
        request.user.profile.save()

    # Add delivery cost if no subscription
    if subscription_exists:
        delivery_cost = 0

    # Add products to cart and apply discounts to individual products
    for item_id, item_data in cart.items():
        product = get_item_from_item_id(item_id)

        if isinstance(product, Subscription):
            total += item_data * product.price

        elif isinstance(product, Program):
            total_item_price = item_data * product.total_final_price
            if subscription_exists:
                sub = request.user.profile.subscription.program_discount
                total_item_price, members_discount = \
                    apply_subscription_discount(
                        subscription_discount=sub,
                        product=product,
                        total_item_price=total_item_price
                    )
                total_members_discount += members_discount
            total += total_item_price
        else:
            total_item_price = item_data * product.total_final_price
            if subscription_exists:
                sub = request.user.profile.subscription.product_discount
                total_item_price, members_discount = \
                    apply_subscription_discount(
                        subscription_discount=sub,
                        product=product,
                        total_item_price=total_item_price
                    )
                total_members_discount += members_discount
            total += total_item_price

        product_count += item_data
        cart_items.append({
            'item_id': int(item_id),
            'quantity': item_data,
            'product': product,
        })

    # Add delivery cost if no products in cart
    if len(cart_items) == 0:
        delivery_cost = 0

    total += delivery_cost

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery_cost': delivery_cost,
        "discount": round(total_members_discount, 2),
    }

    return context
