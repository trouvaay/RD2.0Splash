from django.db import models
from django.db.models import Q
from django.conf import settings

from raredoor.models import AbstractImageModel


class Merchant(models.Model): # UUIDModel
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to=Q(profile__is_merchant=True), null=True, blank=True)
    address = models.ForeignKey('raredoor.PostalAddress', blank=True, null=True, default=None)
    contact_info = models.ForeignKey('raredoor.ContactInfo', blank=True, null=True, default=True)
    website = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class Retailer(Merchant):
    legal_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)


class RetailerImage(AbstractImageModel):
    retailer = models.ForeignKey(Retailer, related_name='images')
    is_logo = models.BooleanField(default=False)


class Store(Merchant):
    retailer = models.ForeignKey(Retailer, related_name='stores')
    has_returns = models.BooleanField(default=False)
    commission_fee = models.DecimalField(blank=False, null=False, max_digits=8, decimal_places=2)
    transaction_fee = models.DecimalField(blank=False, null=False, max_digits=8, decimal_places=2)
    order_prefix = models.CharField(max_length=4, unique=True, blank=False, null=False, help_text='This will be pre-pended to all orders from this retailer')



class Discount(models.Model):

    RETAILER_SPECIFIC = 'RETAILER_SPECIFIC'
    GENERAL = 'GENERAL'

    DISCOUNT_TYPES = (
        (RETAILER_SPECIFIC, 'Retailer-specific promo'),
        (GENERAL, 'General discount'),
    )

    name = models.CharField(max_length=100, blank=False, null=False, help_text='e.g. Get $10 off your $50 order')
    short_terms = models.TextField(max_length=1000, blank=True, null=False, default='', help_text='This is a short vertion of the terms that we can show to the user e.g. on a front page where they might actually read it.')
    terms = models.TextField(max_length=10000, blank=True, null=False, default='', help_text='This is the "fine print", explaining in every details the terms of the promotion')

    # having a special field would allow us to figure out
    # how each 'kind' of offer should be handled
    discount_type = models.CharField(max_length=50, choices=DISCOUNT_TYPES, blank=False, null=False, db_index=True, help_text='This field determines how offer is applied: e.g. Retailer-specific discounts are only for the goods sold by that retailer')
    retailer = models.ForeignKey(Retailer, blank=True, null=True, default=None, related_name='discounts')

    # The following fields are used to determine whether or not this discount is valid. The most imporant one
    # is 'is_active' which takes precedence over any other fields when determining whether or not the offer is valid
    # e.g. start/end time, uses_per_user, or uses_total would only have meaning the offer is active
    # making default=False, so that we have to explicitly enable it
    is_active = models.BooleanField(blank=False, null=False, default=False, help_text='This is On/Off switch for the offer')
    start_time = models.DateTimeField(blank=True, null=True, default=None, help_text='When offer becomes available')
    end_time = models.DateTimeField(blank=True, null=True, default=None, help_text='When offer expires')
    uses_per_user = models.IntegerField(blank=False, null=False, help_text='Positive number - how many times this offer can be used per user, -1 - unlimited')
    uses_total = models.IntegerField(blank=False, null=False, help_text='Positive number - total number of times this offer can be used, -1 - unlimited')

    # codes must be unique, but they are also optional
    # we will handle the uniqueness in the 'save' method
    # because django can't handle unique and optinally empty fields
    # the way one would expect. I've ran into this long time ago,
    # but the issue still remains to this day see my stackoverflow question for details
    # http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
    code = models.CharField(max_length=100, blank=True, default='', db_index=True, help_text='Code for the promotion. Codes are case insensitive, e.g. PROMO2015 and Promo2015 is the same thing, so cannot create two different codes like that.')

    # The following fields determine the actual value of the discount
    # Either fixed_amount_off or percent_off must be set and be non-zero
    # we will handle this constraint in the save() method
    fixed_amount_off = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text='e.g. 20 means $20 off')
    fixed_amount_off_minimum_order = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text='Order minimum that is required (if any) to get this discount. 0 means there is not minimum. This is applicable only when fixed_amount_off is set')
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None, help_text='Expressed as percentage, e.g. 10 means 10%% off')
    percent_off_limit = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None, help_text='Limits the maximum dollar value of the Percent discount off. This is applicable only when percent_off is set')

