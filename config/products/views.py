# your_app_name/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404, Http404

from .models import Product, ProductVariant
from .serializers import ProductSerializer, ProductVariantSerializer

# --- Product Views ---

@api_view(['GET'])
def product_list(request):
    """
    List all products.
    """
    products = Product.objects.all().order_by('name_en')
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    """
    Retrieve a product instance.
    """
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def product_variants_list(request, pk):
    """
    List all variants for a specific product.
    """
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.all().order_by('size', 'color') # Added ordering for consistency
    serializer = ProductVariantSerializer(variants, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def product_variant_detail(request, product_pk, variant_pk):
    """
    Retrieve a specific variant for a specific product.
    """
    try:
        # First, ensure the product exists
        product = get_object_or_404(Product, pk=product_pk)
        # Then, get the variant ensuring it belongs to that product
        variant = get_object_or_404(ProductVariant, product=product, pk=variant_pk)
    except Http404:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductVariantSerializer(variant, context={'request': request})
    return Response(serializer.data)


# --- Product Variant Views (Global) ---

@api_view(['GET'])
def variant_list(request):
    """
    List all product variants globally.
    """
    variants = ProductVariant.objects.all().order_by('product__name_en', 'size', 'color')
    serializer = ProductVariantSerializer(variants, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def variant_detail(request, pk):
    """
    Retrieve a product variant instance by its global ID.
    """
    variant = get_object_or_404(ProductVariant, pk=pk)
    serializer = ProductVariantSerializer(variant, context={'request': request})
    return Response(serializer.data)