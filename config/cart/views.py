# cart/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.shortcuts import get_object_or_404
from django.db.models import F

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from product.models import Product # Import your Product model

# --- Cart Views ---

@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) # Adjust permissions as needed
def cart_list_create(request):
    """
    GET: List all carts (admin only usually, or user's own cart if authenticated).
    POST: Create a new cart.
    """
    if request.method == 'GET':
        # For authenticated user, show their cart. For anonymous, show nothing or allow creating.
        if request.user.is_authenticated:
            carts = Cart.objects.filter(user=request.user)
        else:
            # You might not want to list all anonymous carts without specific IDs
            # For simplicity, returning empty if anonymous GET for list.
            carts = Cart.objects.none() 
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # If user is authenticated, ensure they don't already have a cart
        if request.user.is_authenticated and Cart.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "User already has an active cart. Use PATCH to update it, or GET to retrieve it."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
@permission_classes([AllowAny]) # Adjust permissions as needed (e.g., IsOwnerOrAdmin)
def cart_detail_update(request, pk):
    """
    GET: Retrieve a single cart by ID.
    PATCH: Update a cart (e.g., its user, though usually handled by items).
    """
    cart = get_object_or_404(Cart, pk=pk)

    # Permission check: Ensure user can access this cart
    if request.user.is_authenticated and cart.user and cart.user != request.user:
        return Response(
            {"detail": "You do not have permission to access this cart."},
            status=status.HTTP_403_FORBIDDEN
        )
    # If anonymous cart, allow access (or implement token-based access for anonymous)
    if not request.user.is_authenticated and cart.user:
        return Response(
            {"detail": "This is an authenticated user's cart. Login required."},
            status=status.HTTP_403_FORBIDDEN
        )


    if request.method == 'GET':
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        # For cart PATCH, usually you wouldn't directly patch 'items' here
        # Items are patched via specific cart item endpoints.
        # This PATCH could be for associating an anonymous cart with a user after login.
        serializer = CartSerializer(cart, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Cart Item Views ---

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def cart_item_list_create(request, cart_pk):
    """
    GET: List all items in a specific cart.
    POST: Add a new item to a specific cart.
    """
    cart = get_object_or_404(Cart, pk=cart_pk)

    # Permission check for the cart
    if request.user.is_authenticated and cart.user and cart.user != request.user:
        return Response(
            {"detail": "You do not have permission to modify this cart."},
            status=status.HTTP_403_FORBIDDEN
        )
    if not request.user.is_authenticated and cart.user:
        return Response(
            {"detail": "This is an authenticated user's cart. Login required."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'GET':
        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data.get('quantity', 1)
            
            product = get_object_or_404(Product, pk=product_id, is_active=True)

            # Check if item already exists in cart, then update quantity
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity = F('quantity') + quantity # Use F object for atomic update
                cart_item.save(update_fields=['quantity'])
                cart_item.refresh_from_db() # Reload to get the updated quantity
            
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def cart_item_detail_update_delete(request, cart_pk, item_pk):
    """
    GET: Retrieve a single item from a specific cart.
    PATCH: Update quantity of an item in a cart.
    DELETE: Remove an item from a cart.
    """
    cart = get_object_or_404(Cart, pk=cart_pk)
    cart_item = get_object_or_404(CartItem, pk=item_pk, cart=cart)

    # Permission check for the cart
    if request.user.is_authenticated and cart.user and cart.user != request.user:
        return Response(
            {"detail": "You do not have permission to modify this cart."},
            status=status.HTTP_403_FORBIDDEN
        )
    if not request.user.is_authenticated and cart.user:
        return Response(
            {"detail": "This is an authenticated user's cart. Login required."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'GET':
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            # Only allow 'quantity' to be updated for cart items via PATCH
            if 'product_id' in serializer.validated_data:
                 return Response({"detail": "Product cannot be changed directly via PATCH. Remove and add new item."},
                                 status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)