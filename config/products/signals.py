
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Product, ProductVariant

# @receiver(post_save, sender=Product)
# def create_main_variant(sender, instance, created, **kwargs):
#     """
#     Automatically create the first variant for a new Product.
#     """
#     if created and not instance.variants.exists():
#         # First create the variant without colors
#         variant = ProductVariant.objects.create(
#             product=instance,
#             varient_size=instance.size,
#             varient_stock=instance.stock,
#             price_override=None,
#             sku=f"default-{instance.id}"
#         )

#         # If product has colors, assign them AFTER creation
#         if instance.color.exists():
#             variant.varient_color.set(instance.color.all())   # copy all product colors
