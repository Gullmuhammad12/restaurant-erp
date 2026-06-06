from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import Decimal
from .models import Order, OrderItem, MenuItemIngredient, Ingredient, Notification

@receiver(post_save, sender=OrderItem)
def update_order_totals(sender, instance, created, **kwargs):
    """Recalculate order totals when items change"""
    order = instance.order
    total = sum(item.subtotal for item in order.items.all())
    order.total_amount = total
    order.save()

@receiver(pre_save, sender=Order)
def deduct_inventory_on_preparing(sender, instance, **kwargs):
    """When order status changes to 'preparing', deduct ingredients"""
    if instance.pk:
        old = sender.objects.get(pk=instance.pk)
        if old.status != 'preparing' and instance.status == 'preparing':
            # Deduct stock for each order item
            for order_item in instance.items.all():
                recipes = MenuItemIngredient.objects.filter(menu_item=order_item.menu_item)
                for recipe in recipes:
                    ingredient = recipe.ingredient
                    required = recipe.quantity_required * order_item.quantity
                    if ingredient.current_stock < required:
                        # Create notification for low stock
                        Notification.objects.create(
                            message=f"Insufficient stock for {ingredient.name} (needs {required} {ingredient.unit}, only {ingredient.current_stock} left)"
                        )
                        # Optionally raise validation error, but we'll deduct as much as possible
                        # To keep it safe, we will deduct min of available
                        to_deduct = min(required, ingredient.current_stock)
                    else:
                        to_deduct = required
                    ingredient.current_stock -= to_deduct
                    ingredient.save()
                    # Low stock notification
                    if ingredient.is_low_stock():
                        Notification.objects.create(
                            message=f"Low stock alert: {ingredient.name} is at {ingredient.current_stock} {ingredient.unit}"
                        )