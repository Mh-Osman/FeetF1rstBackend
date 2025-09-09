from django.contrib import admin
from .models import Product, ProductVariant , AvailableSize, Category, Brand, Color


admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(AvailableSize)              
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
# Register your models here.
