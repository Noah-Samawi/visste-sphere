"""Products URL Configuration"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product', views.AddProductPage.as_view(), name='add_product'),
    path('edit_product/<int:pk>/', views.EditProductPage.as_view(), name='edit_product'),
]
