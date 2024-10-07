"Utility functions for products app"

from django.db.models import Q
from products.models import Category


def filter_and_sort_products(products, request):

    """Filter and sort items based on user's request/query parameters"""

    query = None
    categories = None
    category = None
    sort = None
    direction = 'asc'

    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        category = categories[0]
        products = products.filter(category__name__in=categories)
        categories = Category.objects.filter(name__in=categories).first()

    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            query = ''
        # Cant do triple union type pylint error
        queries = (
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query)
        )

        products = products.filter(queries)

    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sortkey = f'-{sortkey}'
        products = products.order_by(sortkey)
        # Sort key based on total final price not price
        if sortkey == 'price':
            products = sorted(products, key=lambda p: p.total_final_price)
        if sortkey == '-price':
            products = sorted(
                        products,
                        key=lambda p: p.total_final_price,
                        reverse=True)
        if sortkey == 'sale':
            products = products.filter(sale__gt=0)

    filtered_products = products

    return filtered_products, query, categories, sort, direction, category
