from django.db import models
from django.conf import settings

from raredoor.models import TimestampedModel


def generate_order_number(order):
    """
    Generates new order number in the following format:

    <RETAILER PREFIX><NUMERIC PART>

    RETAILER PREFIX - string containing letters, comes from order.product.retailer.order_prefix
    NUMERIC PART - number that along with retailer prefix makes the order unique
    """
    pass


class BaseOrder(TimestampedModel):
    """
    Contains the fields that are same between Order and Offer
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False) #, related_name='user_orders')
    shipping_address = models.ForeignKey('raredoor.PostalAddress')
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text='Total price of all items before discounts, shipping  and taxes')
    taxes = models.DecimalField(max_digits=8, decimal_places=2, blank=None, null=None, default=0.00, help_text='Taxes in dollars')
    shipping_price = models.DecimalField(max_digits=8, decimal_places=2, blank=None, null=None, default=0.00, help_text='Price of shipping')
    total_transaction_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text='Total purchase price the user paid including promotions and taxes')

    class Meta:
        abstract = True


class BaseOrderItem(TimestampedModel):
    """Contains the fields that are same between OrderItem, CartItem and Offer"""

    product_variation = models.ForeignKey('product.ProductVariation', blank=False, null=False, related_name='product_variation_%(class)s')
    store = models.ForeignKey('merchant.Store', blank=False, null=False, related_name='store_%(class)s')
    quantity = models.PositiveIntegerField(blank=False, null=False)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text='Price of the product before taxes and discounts')

    class Meta:
        abstract = True


class Order(BaseOrder):
    order_number = models.CharField(primary_key=True, max_length=20, blank=False, null=False, default=generate_order_number, editable=False)


class OrderItem(BaseOrderItem):
    order = models.ForeignKey(Order, related_name='items')


class Offer(BaseOrderItem): # class Offer(BaseOrderItem, BaseOrder): # TODO: should be only one of the classes
    is_active = models.BooleanField(default=True)
    expiration_timestamp = models.DateTimeField(blank=False, null=False, help_text='When this offer expires')


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='cart')


class CartItem(BaseOrderItem):
    cart = models.ForeignKey(Cart, related_name='items')


class DiscountRedemption(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_redemptions')
    discount = models.ForeignKey('merchant.Discount', blank=False, null=False, related_name='discount_redemptions')
    order = models.ForeignKey(Order, blank=False, null=False, related_name='order_discount_redemptions')
    timestamp = models.DateTimeField(blank=False, null=False, help_text='When this was redeemed')
    total_before_discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text='Total dollar amount before applying any promotinal discounts to the order')
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text='Discount dollar amount')


