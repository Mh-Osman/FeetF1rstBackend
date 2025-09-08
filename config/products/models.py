from django.db import models

class Product(models.Model):
    # Category choices
    CATEGORY_CHOICES = [
        ("running_shoes", "Running Shoes"),
        ("cycling_shoes", "Cycling Shoes"),
        ("hockey_shoes", "Hockey Shoes"),
        ("ski_boots", "Ski Boots"),
        ("basketball_shoes", "Basketball Shoes"),
        ("golf_shoes", "Golf Shoes"),
        ("football_shoes", "Football Shoes"),
        ("tennis_shoes", "Tennis Shoes"),
        ("climbing_shoes", "Climbing Shoes"),
        ("casual_sneaker", "Casual Sneakers"),
        ("dress_shoes", "Dress Shoes"),
        ("comfortable_shoes", "Comfortable Shoes"),
        ("sandals", "Sandals"),
        ("work_shoes", "Work Shoes"),
        ("miscellaneous", "Miscellaneous"),
    ]

    # Category
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    # English
    name_en = models.CharField(max_length=200)
    description_en = models.TextField(blank=True, null=True)

    # Italian
    name_it = models.CharField(max_length=200, blank=True, null=True)
    description_it = models.TextField(blank=True, null=True)

    # German
    name_de = models.CharField(max_length=200, blank=True, null=True)
    description_de = models.TextField(blank=True, null=True)


    # Product details
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)   # whether visible on store

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_en} ({self.get_category_display()})"

class ProductVariant(models.Model):
    # Link to the main Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

    # Variant attributes - now plain CharFields without choices
    size = models.CharField(max_length=50, blank=True, null=True) # Increased max_length for flexibility
    color = models.CharField(max_length=50, blank=True, null=True)

    # Specific stock for this variant
    stock = models.PositiveIntegerField(default=0)
    # You might want to override the price for specific variants
    price_override = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # A unique SKU (Stock Keeping Unit) for each variant
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)

    # Image for this specific variant
    image = models.ImageField(upload_to="product_variants/", blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures that a product cannot have two identical variants (e.g., same size and color)
        # Note: With no choices, you'll need to be consistent with input (e.g., always "Red", not sometimes "red").
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        variant_parts = [self.product.name_en]
        if self.color:
            variant_parts.append(self.color)
        if self.size:
            variant_parts.append(self.size)
        return " - ".join(variant_parts)

    def get_price(self):
        """Returns the variant's price, or the product's price if not overridden."""
        return self.price_override if self.price_override is not None else self.product.price