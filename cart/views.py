"""Cart Views"""
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages

from products.models import Product
from profiles.models import Subscription


from .utils import get_item_from_item_id


def view_cart(request):
    """ A view that renders the cart contents page """

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    quantity = request.POST.get('quantity')
    redirect_url = request.POST.get('redirect_url')

    product = get_item_from_item_id(item_id)
    cart = request.session.get('cart', {})

    # Server side validation to prevent negative or zero quantities
    if quantity is not None and int(quantity) <= 0 \
            and isinstance(product, Product):
        messages.error(request, 'Quantity must be greater than 0')
        return redirect(redirect_url)

    # Remove previous subscription from cart if a new subscription is added
    if isinstance(product, Subscription):
        for cart_item_id in list(cart.keys()):
            if int(cart_item_id) >= 51:
                del cart[cart_item_id]

    if item_id in list(cart.keys()) and quantity:
        cart[item_id] += int(quantity)
        messages.success(request,
                         f'Updated {product.name} quantity to {cart[item_id]}')
    elif quantity:
        cart[item_id] = int(quantity)
        messages.success(request,
                         f'Added {cart[item_id]} {product.name} to your cart')
    else:
        cart[item_id] = 1
        messages.success(request, f'Added {product.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    # Server side validation to prevent negative or zero quantities
    if int(quantity) <= 0:
        messages.error(request, 'Quantity must be greater than 0')
        return redirect(redirect_url)

    cart = request.session.get('cart', {})

    product = get_object_or_404(Product, pk=item_id)

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request,
                         f'Updated {product.name} quantity to {cart[item_id]}')
    else:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""

    cart = request.session.get('cart', {})
    redirect_url = request.POST.get('redirect_url')

    product = get_item_from_item_id(item_id)

    try:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
