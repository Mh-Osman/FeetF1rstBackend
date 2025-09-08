from django.contrib import admin
from .models import Product, ProductVariant

# 1. Define the Inline class for ProductVariant
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1 # Number of empty forms to display for new variants
    # Optional: Customize the fields displayed in the inline
    fields = ('size', 'color', 'stock', 'price_override', 'sku', 'image')
    # You can also set readonly_fields here if you want certain variant fields uneditable in the inline
    # readonly_fields = ('sku',) # Example: make SKU read-only after creation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name_en",
        "category",
        "price",
        "is_active",
        "display_variants_count" # Add a custom method to show variant count
    )
    search_fields = ("name_en", "name_it", "name_de", "name_fr")
    list_filter = ("category", "is_active")

    # 2. Add the inline to the ProductAdmin
    inlines = [ProductVariantInline]

    # Custom method to display the count of variants for each product
    def display_variants_count(self, obj):
        return obj.variants.count()
    display_variants_count.short_description = "Variants" # Column header in list_display


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "color",
        "size",
        "stock",
        "get_price", # This method is defined on your ProductVariant model
        "sku",
        "image_tag" # Add a custom method to display the image thumbnail
    )
    search_fields = ("product__name_en", "color", "size", "sku")
    list_filter = ("product__category", "color", "size") # Filter by product category, color, size
    ordering = ('product__name_en', 'color', 'size') # Order for better readability

    # Custom method to display a thumbnail of the variant image in the admin list view
    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            from django.utils.html import format_html
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain;" />'.format(obj.image.url))
        return "No Image"
    image_tag.short_description = "Image"