from django.db import models
from django.conf import settings
from products.models import Product, ProductVariant


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     if self.user:
        return f"Cart ({self.user.full_name})"
     return f"Anonymous Cart {self.id}"
  
    @property
    def total_items(self):
        return sum(
            item.main_product_quantity + (item.variant_product_quantity if item.product_variant else 0)
            for item in self.items.all()
        )

    @property
    def total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    main_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    main_product_quantity = models.PositiveIntegerField(default=0)

    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=True, blank=True
    )
    variant_product_quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('cart', )

    def __str__(self):
        if self.product_variant:
            return f"{self.main_product.name_en})"
        return f"{self.main_product.name_en} x {self.main_product_quantity}"

    def get_total_price(self):
        total = self.main_product.price * self.main_product_quantity
        if self.product_variant:
            total += self.product_variant.price * self.variant_product_quantity
        return total
