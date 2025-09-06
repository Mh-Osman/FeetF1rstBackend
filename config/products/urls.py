# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Product Categories
    path('categories/', views.category_list_create, name='category-list-create'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),

    # Product SubCategories
    path('subcategories/', views.subcategory_list_create, name='subcategory-list-create'),
    path('subcategories/<int:pk>/', views.subcategory_detail, name='subcategory-detail'),

    # Brands
    path('brands/', views.brand_list_create, name='brand-list-create'),
    path('brands/<int:pk>/', views.brand_detail, name='brand-detail'),

    # Products
    path('products/', views.product_list_create, name='product-list-create'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),

    # Product Images (optional, often managed via product views or admin)
    path('product-images/', views.product_image_list_create, name='product-image-list-create'),
    path('product-images/<int:pk>/', views.product_image_detail, name='product-image-detail'),

    # Product Variants (optional, often managed via product views or admin)
    path('product-variants/', views.product_variant_list_create, name='product-variant-list-create'),
    path('product-variants/<int:pk>/', views.product_variant_detail, name='product-variant-detail'),
]