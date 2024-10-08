"""Program Views"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Program

from products.utils import filter_and_sort_products
from cart.contexts import cart_contents


def all_programs(request):
    """ A view to show all programs, including sorting and search queries """
    programs = Program.objects.all()

    filtered_products, query, categories, sort, direction, category = \
        filter_and_sort_products(products=programs, request=request)

    context = {
        'programs': filtered_products,
        'search_term': query,
        'current_categories': categories,
        'sort': sort,
        'direction': direction,
        'query': query,
        'category': category
    }

    return render(request, 'programs/programs.html', context)


def program_detail(request, program_id):
    """ A view to show individual product details """
    purchased = False
    program = get_object_or_404(Program, pk=program_id)
    related_programs = (Program.objects
                        .filter(category=program.category)
                        .exclude(pk=program.id))

    # Loop through orders to check if program has been purchased
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            orders = request.user.profile.orders.all()
        else:
            orders = []
    else:
        orders = []

    for order in orders:
        for item in order.lineitems.all():
            if item.content_object.id == program_id:
                purchased = True

    # check to see if program is in cart
    current_cart = cart_contents(request)
    in_cart = any(
        item['product'].id == program.id
        for item in current_cart['cart_items']
    )

    # check to see if senior dev subscription is in cart
    senior_dev_in_cart = any(
        item['product'].id == 54
        for item in current_cart['cart_items'])

    # Add purchase if senior dev subscription active and not in cart
    if request.user.is_authenticated:
        subscription = request.user.profile.subscription
        if subscription:
            if subscription.pk == 54 and not senior_dev_in_cart:
                purchased = True

    paginator = Paginator(related_programs, 4)
    page = request.GET.get('page')

    try:
        related_programs = paginator.page(page)
    except PageNotAnInteger:
        related_programs = paginator.page(1)
    except EmptyPage:
        # If empty page deliver last page.
        related_programs = paginator.page(paginator.num_pages)

    context = {
        'program': program,
        'related_programs': related_programs,
        'in_cart': in_cart,
        "purchased": purchased
    }

    return render(request, 'programs/program_detail.html', context)
