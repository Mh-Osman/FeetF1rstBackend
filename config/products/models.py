from django.db import models
from django.db import models

class ProductCategory(models.Model):
    """
    Represents a top-level category for shoes, e.g., "Everyday Shoes", "Sports Shoes".
    """
    name_en = models.CharField(max_length=100, unique=True, verbose_name="Category Name (English)")
    name_it = models.CharField(max_length=100, unique=True, verbose_name="Category Name (Italian)")
    name_de = models.CharField(max_length=100, unique=True, verbose_name="Category Name (German)") # Added German field

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        # Ordering by English name for default backend display
        ordering = ['name_en']

    def __str__(self):
        return self.name_en # Still using English name for default representation




class ProductSubCategory(models.Model):
    """
    Represents a sub-category for shoes, e.g., "Running Shoes" under "Sports Shoes".
    """
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Parent Category"
    )
    name_en = models.CharField(max_length=100, unique=True, verbose_name="Sub-Category Name (English)")
    name_it = models.CharField(max_length=100, unique=True, verbose_name="Sub-Category Name (Italian)")
    name_de = models.CharField(max_length=100, unique=True, verbose_name="Sub-Category Name (German)") # Added German field

    class Meta:
        verbose_name = "Product Sub-Category"
        verbose_name_plural = "Product Sub-Categories"
        # Ensure sub-category names are unique within a parent category using the English name
        unique_together = ('category', 'name_en')
        ordering = ['category__name_en', 'name_en']

    def __str__(self):
        return f"{self.category.name_en} - {self.name_en}"
    


class Brand(models.Model):
    """
    Represents a shoe brand.
    """
    name = models.CharField(max_length=100, unique=True) # Brand name is usually universal
    logo = models.ImageField(upload_to='brands/', blank=True, null=True) # Requires Pillow

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Product(models.Model):
    """
    Represents an individual shoe product.
    """
    name_en = models.CharField(max_length=255, verbose_name="Product Name (English)")
    name_it = models.CharField(max_length=255, verbose_name="Product Name (Italian)")
    name_de = models.CharField(max_length=255, verbose_name="Product Name (German)") # Added German field
    description_en = models.TextField(blank=True, verbose_name="Description (English)")
    description_it = models.TextField(blank=True, verbose_name="Description (Italian)")
    description_de = models.TextField(blank=True, verbose_name="Description (German)") # Added German field
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    subcategory = models.ForeignKey(
        ProductSubCategory,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    SKU = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Stock Keeping Unit")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    number_of_reviews = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name_en']

    def __str__(self):
        return self.name_en


class ProductImage(models.Model):
    """
    Stores images for a specific product.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/') # Requires Pillow
    alt_text_en = models.CharField(max_length=255, blank=True, verbose_name="Alt Text (English)")
    alt_text_it = models.CharField(max_length=255, blank=True, verbose_name="Alt Text (Italian)")
    alt_text_de = models.CharField(max_length=255, blank=True, verbose_name="Alt Text (German)") # Added German field
    is_main = models.BooleanField(default=False, help_text="Set as the main display image for the product.")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        unique_together = ('product', 'is_main')
        ordering = ['-is_main', 'id'] # Main image first

    def __str__(self):
        # A more descriptive string for backend
        return f"Image for {self.product.name_en} ({'Main' if self.is_main else 'Additional'})"

class ProductVariant(models.Model):
    """
    Represents specific variations of a product, e.g., size and color.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    size = models.CharField(max_length=20) # e.g., "US 10", "EU 42"
    color_en = models.CharField(max_length=50, verbose_name="Color (English)")
    color_it = models.CharField(max_length=50, verbose_name="Color (Italian)")
    color_de = models.CharField(max_length=50, verbose_name="Color (German)") # Added German field
    stock = models.PositiveIntegerField(default=0)
    SKU_variant = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Variant SKU")
    image = models.ImageField(upload_to='product_variants/', blank=True, null=True) # Variant-specific image

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        unique_together = ('product', 'size', 'color_en')
        ordering = ['size', 'color_en']

    def save(self, *args, **kwargs):
        # The SKU_variant generation no longer relies on slugify.
        # You might want a different auto-generation logic for SKU_variant
        # or require it to be manually entered.
        if not self.SKU_variant and self.product.SKU:
            # Simple concatenation without slugify
            self.SKU_variant = f"{self.product.SKU}-{self.size.replace(' ', '')}-{self.color_en.replace(' ', '')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name_en} - Size: {self.size}, Color: {self.color_en}"