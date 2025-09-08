from django.urls import path
from . import views
from .views import product_list, product_detail, product_variants_list, variant_list, variant_detail

urlpatterns = [ 
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    # This URL lists ALL variants belonging to a specific product
    path('products/<int:pk>/variants/', views.product_variants_list, name='product-variants-for-product'),
    # This NEW URL retrieves a specific variant of a specific product
    path('products/<int:product_pk>/variants/<int:variant_pk>/', views.product_variant_detail, name='product-variant-detail'),

    # # Product Variant URLs (Global - for retrieving any variant by its global ID)
    # path('variants/', views.variant_list, name='variant-list'),
    # path('variants/<int:pk>/', views.variant_detail, name='variant-detail'),
]
