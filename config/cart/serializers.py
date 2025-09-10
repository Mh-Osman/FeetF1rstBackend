# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product, ProductVariant
# Import the ProductSerializer from your product app
from products.serializers import ProductListSerializer, ProductVariantSerializer # Assuming you want full product details

# Simplified Product serializer for CartItem, if you don't want all details from ProductListSerializer
class SimpleProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListSerializer.Meta.model # Use the Product model directly
        fields = ['id', 'name_en', 'main_image', 'price', 'discount_price']

# If CartItem refers to ProductVariant instead of Product, adjust this.
# For now, assuming it refers to the primary Product model as per your CartItem model.
# If you decide to link CartItem to ProductVariant, you'll need to adjust `product` field in CartItem model.

class CartItemSerializer(serializers.ModelSerializer):
    # Use SimpleProductInCartSerializer for read-only product details
    # This assumes CartItem.product is a ForeignKey to Product
    product = SimpleProductInCartSerializer(read_only=True) 
    
    # Field for writing: expects product ID
    product_id = serializers.IntegerField(write_only=True) 

    # Field for writing: if you want to select a specific variant for the cart item
    # variant_id = serializers.IntegerField(write_only=True, required=False) # Uncomment if using ProductVariant

    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['id', 'added_at']

    def validate(self, data):
        # Ensure product exists
        product_id = data.get('product_id')
        if not ProductListSerializer.Meta.model.objects.filter(id=product_id, is_active=True).exists():
            raise serializers.ValidationError("Product not found or not active.")
        
        # You might also want to check stock here
        # product_instance = ProductListSerializer.Meta.model.objects.get(id=product_id)
        # if data.get('quantity', 1) > product_instance.stock:
        #     raise serializers.ValidationError("Requested quantity exceeds available stock.")

        # If using variants, you'd add variant validation here too
        # variant_id = data.get('variant_id')
        # if variant_id:
        #     if not ProductVariantSerializer.Meta.model.objects.filter(id=variant_id, product_id=product_id).exists():
        #         raise serializers.ValidationError("Variant not found for this product.")
        return data


class CartSerializer(serializers.ModelSerializer):
    # Use nested CartItemSerializer for read-only items
    items = CartItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True) # Shows username if available
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    # For creation, you might want to automatically link to request.user
    def create(self, validated_data):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            # Check if user already has a cart
            existing_cart = Cart.objects.filter(user=user).first()
            if existing_cart:
                raise serializers.ValidationError("User already has an active cart.")
            validated_data['user'] = user
        else:
            validated_data['user'] = None # For anonymous cart
        return super().create(validated_data)