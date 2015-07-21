from django.db import models
from django.conf import settings

from raredoor.models import UUIDModel, TimestampedModel, AbstractImageModel


class Style(models.Model):
    select = models.CharField(unique=True, max_length=55, default='modern', null=True, blank=True)


class Category(models.Model):
    select = models.CharField(unique=True, max_length=55, default='living', null=True, blank=True)


class Subcategory(models.Model):
    category = models.ForeignKey(Category, blank=False, null=False)
    select = models.CharField(unique=True, max_length=55, default='bar', null=True, blank=True)

    # features are product properties that are specific for a particular type
    # e.g. for beds it could be bed size, for tables that could be number of legs
    # for chairs that would be seat height, etc.
    features = models.ManyToManyField('Feature', blank=True, related_name='subcategories')


class PieceType(models.Model):
    subcategory = models.ForeignKey(Subcategory, blank=False, null=False)
    select = models.CharField(unique=True, max_length=55, default='', null=True, blank=True)
    # features are product properties that are specific for a particular type
    # e.g. for beds it could be bed size, for tables that could be number of legs
    # for chairs that would be seat height, etc.
    features = models.ManyToManyField('Feature', blank=True, related_name='piece_types')


class Color(models.Model):
    select = models.CharField(unique=True, max_length=55, default='blue', null=True, blank=True)

class Material(models.Model):
    select = models.CharField(unique=True, max_length=55, default='leather', null=True, blank=True)


class DeliverySize(models.Model):
    select = models.CharField(unique=True, max_length=55, default='', null=True, blank=True)


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)


class ProductVariationStore(models.Model):
    product_variation = models.ForeignKey('ProductVariation', blank=False, null=False)
    store = models.ForeignKey('merchant.Store', blank=False, null=False)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    minimum_offer_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=None)
    url = models.URLField(null=True, blank=True, max_length=255)
    is_available = models.BooleanField(blank=False, null=False)


class Feature(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    value = models.CharField(max_length=100, blank=False, null=False)


class ProductVariation(models.Model):
    variation_name = models.CharField(max_length=100, blank=True, null=True, help_text='What defines this option, e.g. if Product is a "Pillow" variation name can be "Red" or "Leather"')
    variation_sku = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey('Product', blank=False, null=False, related_name='variations')
    color = models.ManyToManyField(Color, blank=True)
    material = models.ManyToManyField(Material, blank=True)
    is_default = models.BooleanField(blank=False, null=False, default=False)
    stores = models.ManyToManyField('merchant.Store', through=ProductVariationStore, related_name='store_products')

    # shipping properties
    shipping_width = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    shipping_depth = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    shipping_height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    # Dimensions & Attributes
    width = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    diameter = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)


class ProductVariationImage(AbstractImageModel):
    product_variation = models.ForeignKey(ProductVariation, related_name='images')


class Product(UUIDModel, TimestampedModel):

    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    manufacturer_sku = models.CharField(max_length=100, null=True, blank=True)
    upc = models.CharField(max_length=12, null=True, blank=True)

    short_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(null=True, blank=True)

    msrp = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)  # list of tag words
    is_custom = models.BooleanField(default=False)
    is_floor_model = models.BooleanField(default=False)
    is_vintage = models.BooleanField(blank=False, null=False)
    is_hand_made = models.BooleanField(blank=False, null=False)

    # Categorization
    style = models.ManyToManyField(Style, blank=True, verbose_name='style')
    category = models.ManyToManyField(Category, blank=True)
    subcategory = models.ManyToManyField(Subcategory, blank=True)
    piece_type = models.ManyToManyField(PieceType, blank=True)
    delivery_size = models.ManyToManyField(DeliverySize, blank=True)

    # Availability
    added_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_recent = models.BooleanField(default=True)
    hours_left = models.IntegerField(default=settings.SHELF_LIFE, null=True, blank=True)
    click_count = models.IntegerField(blank=False, null=False, default=0)
    display_score = models.IntegerField(blank=False, null=False, default=0)

