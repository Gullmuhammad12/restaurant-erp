# core/utils.py
import uuid
import re
from django.utils.text import slugify

def generate_unique_slug(instance, source_field, slug_field='slug', max_length=50):
    """
    Generate a unique slug for a model instance.
    
    Args:
        instance: Model instance
        source_field: Name of the field to base the slug on (e.g., 'name', 'full_name')
        slug_field: Name of the slug field (default 'slug')
        max_length: Maximum length of the slug before truncation
    
    Returns:
        str: Unique slug
    """
    # Get the source value
    source_value = getattr(instance, source_field)
    if not source_value:
        source_value = str(instance.pk) if instance.pk else uuid.uuid4().hex
    
    # Create base slug
    base_slug = slugify(source_value)[:max_length]
    if not base_slug:
        base_slug = uuid.uuid4().hex[:8]
    
    # Ensure uniqueness
    unique_slug = base_slug
    ModelClass = instance.__class__
    counter = 1
    while ModelClass.objects.filter(**{slug_field: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{base_slug[:max_length-3]}-{counter}"
        counter += 1
    
    return unique_slug

def generate_random_slug(prefix='', length=8):
    """
    Generate a completely random, URL-safe slug.
    
    Args:
        prefix: Optional prefix (e.g., 'order-', 'ingredient-')
        length: Length of random part
    
    Returns:
        str: Random slug
    """
    random_part = uuid.uuid4().hex[:length]
    if prefix:
        return f"{prefix}{random_part}"
    return random_part

def sanitize_phone_number(phone):
    """
    Remove non-digit characters from a phone number.
    
    Args:
        phone: Raw phone string
    
    Returns:
        str: Digits only
    """
    if not phone:
        return ''
    return re.sub(r'\D', '', phone)

def format_currency(amount, symbol='$'):
    """
    Format a decimal amount as currency string.
    
    Args:
        amount: Decimal or float
        symbol: Currency symbol
    
    Returns:
        str: Formatted currency (e.g., "$12.50")
    """
    if amount is None:
        amount = 0
    return f"{symbol}{float(amount):,.2f}"

def truncate_string(text, max_length=50, suffix='...'):
    """
    Truncate a string to a maximum length with suffix.
    
    Args:
        text: Input string
        max_length: Maximum allowed length
        suffix: Suffix to append if truncated
    
    Returns:
        str: Truncated string
    """
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def calculate_tax(amount, tax_rate=0.10):
    """
    Calculate tax amount.
    
    Args:
        amount: Decimal or float
        tax_rate: Tax rate as decimal (default 0.10 = 10%)
    
    Returns:
        Decimal: Tax amount
    """
    from decimal import Decimal
    return Decimal(str(amount)) * Decimal(str(tax_rate))