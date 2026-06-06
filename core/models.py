import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# ---------- Custom User Manager ----------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

# ---------- Custom User Model ----------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('kitchen', 'Kitchen Staff'),
        ('waiter', 'Waiter'),
    ]
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='waiter')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

# ---------- Staff Profile (shift tracking) ----------
class StaffProfile(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Morning (6am-2pm)'),
        ('evening', 'Evening (2pm-10pm)'),
        ('night', 'Night (10pm-6am)'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, default='morning')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.user.full_name}-{uuid.uuid4().hex[:6]}")
            self.slug = base_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.full_name} ({self.get_shift_display()})"

# ---------- Menu Item ----------
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{uuid.uuid4().hex[:8]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ---------- Ingredient ----------
class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('pcs', 'Pieces'),
    ]
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    low_stock_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=5)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{uuid.uuid4().hex[:8]}")
        super().save(*args, **kwargs)

    def is_low_stock(self):
        return self.current_stock <= self.low_stock_threshold

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"

# ---------- Recipe (MenuItem -> Ingredient) ----------
class MenuItemIngredient(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('menu_item', 'ingredient')

    def __str__(self):
        return f"{self.menu_item.name} needs {self.quantity_required} {self.ingredient.unit} of {self.ingredient.name}"

# ---------- Order (slug-based) ----------
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('dine_in', 'Dine-in'),
        ('takeaway', 'Takeaway'),
        ('delivery', 'Delivery'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    slug = models.SlugField(unique=True, blank=True, editable=False)
    table_number = models.CharField(max_length=10, blank=True, help_text="For dine-in")
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="10% tax")
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"order-{uuid.uuid4().hex[:12]}")
        # Recalculate totals (defensive)
        self.tax = self.total_amount * Decimal('0.10')
        self.net_amount = self.total_amount + self.tax
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.slug[:8]}"

# ---------- Order Item ----------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot price
    special_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.order.slug[:8]} - {self.menu_item.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.quantity * self.price

# ---------- Notification (for low stock, etc.) ----------
class Notification(models.Model):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

# ---------- Signal: Deduct Inventory When Order Status Becomes 'Preparing' ----------
@receiver(post_save, sender=Order)
def deduct_inventory_on_preparing(sender, instance, **kwargs):
    if instance.status == 'preparing':
        for order_item in instance.items.all():
            recipes = MenuItemIngredient.objects.filter(menu_item=order_item.menu_item)
            for recipe in recipes:
                ingredient = recipe.ingredient
                required = recipe.quantity_required * order_item.quantity
                if ingredient.current_stock < required:
                    Notification.objects.create(
                        message=f"Insufficient stock for {ingredient.name} (needs {required} {ingredient.unit}, only {ingredient.current_stock} left)"
                    )
                    # Deduct what we have to avoid negative stock
                    to_deduct = min(required, ingredient.current_stock)
                else:
                    to_deduct = required
                ingredient.current_stock -= to_deduct
                ingredient.save()
                if ingredient.is_low_stock():
                    Notification.objects.create(
                        message=f"Low stock alert: {ingredient.name} is at {ingredient.current_stock} {ingredient.unit}"
                    )