from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductVariant
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductVariantSerializer

# Existing views (keeping them for context, no changes needed)
@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def product_variant_list(request):
    variants = ProductVariant.objects.all().order_by('-created_at')
    serializer = ProductVariantSerializer(variants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_variant_detail(request, pk):
    try:
        variant = ProductVariant.objects.get(pk=pk)
    except ProductVariant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductVariantSerializer(variant)
    return Response(serializer.data)


# NEW VIEWS FOR NESTED VARIANTS

@api_view(['GET'])
def product_variants_by_product(request, product_pk):
    """
    List all variants for a specific product.
    URL: /api/products/<product_pk>/variants/
    """
    try:
        product = Product.objects.get(pk=product_pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    variants = product.variants.all().order_by('id') # Access variants through the related_name
    serializer = ProductVariantSerializer(variants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_variant_detail_by_product(request, product_pk, variant_pk):
    """
    Retrieve a specific variant for a specific product.
    URL: /api/products/<product_pk>/variants/<variant_pk>/
    """
    try:
        # First, ensure the product exists
        product = Product.objects.get(pk=product_pk)
        # Then, find the variant belonging to that product
        variant = product.variants.get(pk=variant_pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ProductVariant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductVariantSerializer(variant)
    return Response(serializer.data)