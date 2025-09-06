# products/admin.py
from django.contrib import admin
from .models import ProductCategory, ProductSubCategory, Brand, Product, ProductImage, ProductVariant

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text_en', 'alt_text_it', 'alt_text_de', 'is_main')

# Inline for Product Variants

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'color_en', 'color_it', 'color_de', 'stock', 'SKU_variant', 'image')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_it', 'name_de') # Removed slug
    # removed prepopulated_fields for slug

@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_it', 'name_de', 'category') # Removed slug
    list_filter = ('category',)
    # removed prepopulated_fields for slug

from django.contrib import admin
from django.utils.html import format_html
from .models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("logo_thumb", "name")
    search_fields = ("name",)
    readonly_fields = ("logo_preview",)

    fieldsets = (
        (None, {"fields": ("name", "logo")}),
        ("Preview", {"fields": ("logo_preview",)}),
    )

    def logo_thumb(self, obj):
        if obj.logo and hasattr(obj.logo, "url"):
            return format_html(
                '<img src="{}" style="height:32px;width:32px;object-fit:contain;border-radius:4px;" />',
                obj.logo.url,
            )
        return "—"
    logo_thumb.short_description = "Logo"
    logo_thumb.admin_order_field = "logo"

    def logo_preview(self, obj):
        if obj.logo and hasattr(obj.logo, "url"):
            return format_html(
                '<img src="{}" style="max-height:200px;max-width:200px;object-fit:contain;border:1px solid #ddd;padding:4px;" />',
                obj.logo.url,
            )
        return "No logo uploaded"
    logo_preview.short_description = "Current logo"
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_de', 'category', 'subcategory', 'brand', 'price', 'is_available')
    list_filter = ('category', 'subcategory', 'brand', 'is_available')
    search_fields = ('name_en', 'name_it', 'name_de', 'description_en', 'description_it', 'description_de', 'SKU')
    # removed prepopulated_fields for slug
    inlines = [ProductImageInline, ProductVariantInline]
    fieldsets = (
        (None, {
            'fields': ('name_en', 'name_it', 'name_de', 'description_en', 'description_it', 'description_de', 'price', 'SKU', 'is_available') # Removed slug
        }),
        ('Categorization', {
            'fields': ('category', 'subcategory', 'brand')
        }), 
        ('Ratings', {
            'fields': ('average_rating', 'number_of_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'average_rating', 'number_of_reviews')