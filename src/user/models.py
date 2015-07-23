from django.db import models
from django.conf import settings

from userena.models import UserenaBaseProfile


class Profile(UserenaBaseProfile): # class Profile(models.Model):
    """
    This is the place where we add any fields when we need a new user property
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='user')

    is_merchant = models.BooleanField(blank=False, null=False, default=False)

    account_balance = models.DecimalField(default='0', max_digits=8, decimal_places=2, help_text='Positive value means credit to the user, negative means user ows to us')
    shipping_address = models.ForeignKey('raredoor.PostalAddress', blank=True, null=True, default=True)
    contact_info = models.ForeignKey('raredoor.ContactInfo', blank=True, null=True, default=True)





