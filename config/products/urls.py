from django.urls import path
from . import views

urlpatterns = [
    # Existing URL patterns
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('variants/', views.product_variant_list, name='product-variant-list'),
    path('variants/<int:pk>/', views.product_variant_detail, name='product-variant-detail'),

    # NEW URL PATTERNS for nested variants
    path('products/<int:product_pk>/variants/', 
         views.product_variants_by_product, 
         name='product-variants-by-product-list'),
         
    path('products/<int:product_pk>/variants/<int:variant_pk>/', 
         views.product_variant_detail_by_product, 
         name='product-variant-detail-by-product'),
]