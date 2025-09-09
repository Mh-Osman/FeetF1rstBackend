from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_it = models.CharField(max_length=100, blank=True, null=True)
    name_de = models.CharField(max_length=100, blank=True, null=True)
    #name_fr = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_it = models.TextField(blank=True, null=True)
    description_de = models.TextField(blank=True, null=True)
    #description_fr = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True)  # e.g., #FFFFFF for white
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_it = models.CharField(max_length=100, blank=True, null=True)
    name_de = models.CharField(max_length=100, blank=True, null=True)
    #name_fr = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_it = models.TextField(blank=True, null=True)
    description_de = models.TextField(blank=True, null=True)
    #description_fr = models.TextField(blank=True, null=True)

    brand = models.ManyToManyField(Brand, related_name='categories', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
#size
class AvailableSize(models.Model):
    size = models.CharField(max_length=20, unique=True)  # "8", "M", "42 EU"
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("UNISEX", "Unisex"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.size} ({self.gender})" if self.gender else self.size
#primary  product
class Product(models.Model):
   
    
    # Category

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    # Brand
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_products', blank=True, null=True)
    color = models.ManyToManyField(Color, related_name='products_main', blank=True, null=True)
    size = models.ForeignKey(AvailableSize, on_delete=models.CASCADE, related_name='size_products', blank=True, null=True)
   
    
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
    
    #discout

    discount_percentage = models.PositiveIntegerField(default=0)  # e.g., 20 for 20% off
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # calculated field
    
    stock = models.PositiveIntegerField(default=0)  # only for products without variants
    
    main_image = models.ImageField(upload_to="products/", blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_en} "
# variant of a product
class ProductVariant(models.Model):
    # Link to the main Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    
    # Variant attributes - now plain CharFields without choices
    varient_color = models.ManyToManyField(Color, related_name='products_variants', blank=True)
    varient_size = models.ForeignKey(AvailableSize, on_delete=models.CASCADE, related_name='size_variants', blank=True, null=True)
    # Specific stock for this variant
    varient_stock = models.PositiveIntegerField(default=0)
    # You might want to override the price for specific variants
    price_override = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # A unique SKU (Stock Keeping Unit) for each variant
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)

    # Image for this specific variant
    image = models.ImageField(upload_to="product_variants/", blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return f"Variant of {self.product.name_en} - SKU: {self.sku}"

    def get_price(self):
        """Returns the variant's price, or the product's price if not overridden."""
        return self.price_override if self.price_override is not None else self.product.price






    
