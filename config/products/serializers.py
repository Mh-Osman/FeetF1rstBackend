from rest_framework import serializers
from .models import Brand, Color, Category, AvailableSize, Product, ProductVariant

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__' # Keeping all fields for the main BrandSerializer

# NEW, SIMPLIFIED BrandSerializer for nested representations
class SimpleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name'] # Only id and name


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class AvailableSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSize
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    # This is the change!
    # Use SimpleBrandSerializer to get id and name for each brand
    brand = SimpleBrandSerializer(many=True, read_only=True) 

    class Meta:
        model = Category
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    varient_color = ColorSerializer(many=True, read_only=True)
    varient_size = AvailableSizeSerializer(read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='get_price', read_only=True)
    
    # NEW FIELD: Get the brand name from the main product
    main_product_brand_name = serializers.CharField(source='product.brand.name', read_only=True)
    main_product_brand_id = serializers.IntegerField(source='product.brand.id', read_only=True) # Optional: if you also want the ID

    # If you want the full simple brand object:
    # main_product_brand = SimpleBrandSerializer(source='product.brand', read_only=True)


    class Meta:
        model = ProductVariant
        fields = [
            'id', 'varient_color', 'varient_size', 'varient_stock',
            'price_override', 'current_price', 'sku', 'image',
            'main_product_brand_name', # Add this new field
            'main_product_brand_id',   # Add this new field (optional)
            # 'main_product_brand', # Use this instead of _name and _id if you want the object
            'created_at', 'updated_at'
        ]

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = SimpleBrandSerializer(read_only=True) # Also updating here if you want simple brand in ProductList
    color = ColorSerializer(many=True, read_only=True)
    size = AvailableSizeSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'brand', 'color', 'size', 'name_en', 'description_en',
            'name_it', 'description_it', 'name_de', 'description_de',
            'price', 'is_active', 'discount_percentage', 'discount_price',
            'stock', 'main_image', 'created_at', 'updated_at'
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = SimpleBrandSerializer(read_only=True) # Also updating here if you want simple brand in ProductDetail
    color = ColorSerializer(many=True, read_only=True)
    size = AvailableSizeSerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True) # Nested serializer for variants

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'brand', 'color', 'size', 'name_en', 'description_en',
            'name_it', 'description_it', 'name_de', 'description_de',
            'price', 'is_active', 'discount_percentage', 'discount_price',
            'stock', 'main_image', 'created_at', 'updated_at', 'variants' # Include variants here
        ]