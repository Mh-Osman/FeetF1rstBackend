# products/serializers.py
from rest_framework import serializers
from .models import ProductCategory, ProductSubCategory, Brand, Product, ProductImage, ProductVariant

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__' # Includes id, name_en, name_it, name_de

class ProductSubCategorySerializer(serializers.ModelSerializer):
    # Optionally, display the parent category's name instead of just its ID
    category_name_en = serializers.ReadOnlyField(source='category.name_en')

    class Meta:
        model = ProductSubCategory
        fields = '__all__' # Includes id, category, name_en, name_it, name_de, category_name_en

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__' # Includes id, name, logo

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__' # Includes id, product, image, alt_text_en, alt_text_it, alt_text_de, is_main

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__' # Includes id, product, size, color_en, color_it, color_de, stock, SKU_variant, image

class ProductSerializer(serializers.ModelSerializer):
    # Nested serializers to include related data in product details
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category_name_en = serializers.ReadOnlyField(source='category.name_en')
    subcategory_name_en = serializers.ReadOnlyField(source='subcategory.name_en')
    brand_name = serializers.ReadOnlyField(source='brand.name')

    class Meta:
        model = Product
        fields = '__all__' # All fields including the nested images, variants and read-only names