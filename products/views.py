"""Product Views"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Category
from .forms import ProductForm


from .utils import filter_and_sort_products


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()

    filtered_products, query, categories, sort, direction, category = \
        filter_and_sort_products(products=products, request=request)

    context = {
        'products': filtered_products,
        'search_term': query,
        'current_categories': categories,
        'sort': sort,
        'direction': direction,
        'query': query,
        'category': category
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    related_products = (
        Product.objects.filter(category=product.category)
        .exclude(pk=product.id)
    )
    # Create pagination if too many related products
    paginator = Paginator(related_products, 4)
    page = request.GET.get('page')

    try:
        related_products = paginator.page(page)
    except PageNotAnInteger:
        related_products = paginator.page(1)
    except EmptyPage:
        # If empty page deliver last page.
        related_products = paginator.page(paginator.num_pages)

    context = {
        'product': product,
        'related_products': related_products

    }

    return render(request, 'products/product_detail.html', context)


class AddProductPage(LoginRequiredMixin, UserPassesTestMixin,
                     generic.CreateView):
    """
    A view for adding products to the store

    """
    template_name = "products/add_product.html"
    success_url = "/products"
    form_class = ProductForm

    def test_func(self):
        """Check if user is admin or moderator"""

        return self.request.user.is_superuser or \
            self.request.user.profile.moderator

    def form_valid(self, form):
        messages.success(self.request, "Product created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       "Product creation failed. Please check your input.")
        return super().form_invalid(form)


class EditProductPage(LoginRequiredMixin, UserPassesTestMixin,
                      generic.UpdateView):
    """
    Allows admins and moderators to to edit or delete products.
    """

    model = Product
    form_class = ProductForm
    template_name = "products/edit_product.html"
    success_url = "/products"

    def post(self, request, *args, **kwargs):
        # Check if the "delete_item" field is present in the POST data
        if "delete_product" in request.POST:
            product = self.get_object()
            if product:
                product.delete()
                messages.success(request, "Product deleted successfully.")
                return redirect("products")

            messages.error(
                request,
                "There was an error with your request, please try again."
            )

        return super().post(request, *args, **kwargs)

    def test_func(self):
        """Check if user is admin or moderator"""

        return self.request.user.is_superuser or \
            self.request.user.profile.moderator

    def form_valid(self, form):
        messages.success(
            self.request,
            "Product updateed successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Product update failed. Please check your input.")
        return super().form_invalid(form)
